import asyncio
import logging
import aiohttp
from typing import Any, Dict, Optional
from .exceptions import APIError, NetworkError

logger = logging.getLogger("navix")

class AiohttpSession:
    """Enterprise-grade network session for reliable communication with Rubika API."""
    def __init__(self, timeout: float = 30.0, max_retries: int = 3):
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.max_retries = max_retries
        self._session: Optional[aiohttp.ClientSession] = None

    async def _get_session(self) -> aiohttp.ClientSession:
        if self._session is None or self._session.closed:
            self._session = aiohttp.ClientSession(timeout=self.timeout)
        return self._session

    async def request(self, method: str, url: str, **kwargs: Any) -> Dict[str, Any]:
        session = await self._get_session()
        retries = 0
        backoff_factor = 1.0

        while retries <= self.max_retries:
            try:
                async with session.request(method, url, **kwargs) as response:
                    # بررسی وضعیت پاسخ HTTP
                    if response.status == 429:
                        # مدیریت Rate Limit از سمت سرور روبیکا
                        retry_after = int(response.headers.get("Retry-After", 5))
                        logger.warning(f"Rubika API Rate Limited. Waiting for {retry_after}s...")
                        await asyncio.sleep(retry_after)
                        retries += 1
                        continue

                    try:
                        data = await response.json()
                    except Exception:
                        text_content = await response.text()
                        raise APIError(f"Invalid JSON response from Rubika: {text_content}")

                    if response.status >= 500:
                        raise APIError(f"Rubika Server Error (Status {response.status}): {data}", status_code=response.status, data=data)

                    return data

            except (aiohttp.ClientError, asyncio.TimeoutError) as net_err:
                retries += 1
                if retries > self.max_retries:
                    logger.error(f"Network connection failed after {self.max_retries} retries: {net_err}")
                    raise NetworkError(f"Failed to connect to Rubika API: {net_err}")

                sleep_time = backoff_factor * (2 ** (retries - 1))
                logger.warning(f"Network glitch occurred ({net_err}). Retrying in {sleep_time}s... (Attempt {retries}/{self.max_retries})")
                await asyncio.sleep(sleep_time)
            except APIError as api_err:
                raise api_err
            except Exception as e:
                logger.error(f"Unexpected error during Rubika request: {e}", exc_info=True)
                raise NetworkError(f"Unexpected network exception: {e}")                             
        raise NetworkError("Max retries exceeded for Rubika API request.")

    async def close(self) -> None:
        if self._session and not self._session.closed:
            await self._session.close()
            self._session = None
