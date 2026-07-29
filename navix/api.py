from __future__ import annotations
from typing import Any, Optional, Dict
from .exceptions import APIError

class API:
    def __init__(self, session: Any, token: Optional[str] = None, **kwargs: Any):
        self.session = session
        self.token = token or getattr(session, 'token', None)
        self.base_url = f"https://bot.rubika.ir/v0/{self.token}" if self.token else "https://bot.rubika.ir/v0"

    async def call(self, method_name: str, data: Optional[Dict[str, Any]] = None) -> Any:
        url = f"{self.base_url}/{method_name}"
        
        # بررسی نوع session برای ارسال درخواست (پشتیبانی از aiohttp یا سایر نشست‌ها)
        if hasattr(self.session, "request"):
            response = await self.session.request("POST", url, json=data or {})
        else:
            raise TypeError("Provided session object does not support 'request' method.")

        if isinstance(response, dict):
            status = response.get("status")
            if status is not None:
                if str(status).upper() not in ("OK", "SUCCESS", "200", "TRUE"):
                    raise APIError(
                        message=response.get("message", "Unknown Rubika API error"),
                        status_code=response.get("status_code", 400),
                        data=response
                    )
        return response
