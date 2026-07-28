import json
from typing import Any, Dict, Optional

class MemoryStorage:
    def __init__(self):
        self.states: Dict[int, str] = {}
        self.data: Dict[int, Dict[str, Any]] = {}

    async def get_state(self, user_id: int) -> Optional[str]:
        return self.states.get(user_id)

    async def set_state(self, user_id: int, state: Optional[str]) -> None:
        if state is None:
            self.states.pop(user_id, None)
        else:
            self.states[user_id] = state

    async def get_data(self, user_id: int) -> Dict[str, Any]:
        return self.data.get(user_id, {})

    async def set_data(self, user_id: int, data: Dict[str, Any]) -> None:
        self.data[user_id] = data

class FileStorage:
    def __init__(self, file_path: str = "navix_fsm.json"):
        self.file_path = file_path

    def _load(self) -> dict:
        try:
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"states": {}, "data": {}}

    def _save(self, data: dict) -> None:
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    async def get_state(self, user_id: int) -> Optional[str]:
        db = self._load()
        return db["states"].get(str(user_id))

    async def set_state(self, user_id: int, state: Optional[str]) -> None:
        db = self._load()
        if state is None:
            db["states"].pop(str(user_id), None)
        else:
            db["states"][str(user_id)] = state
        self._save(db)

    async def get_data(self, user_id: int) -> Dict[str, Any]:
        db = self._load()
        return db["data"].get(str(user_id), {})

    async def set_data(self, user_id: int, data: Dict[str, Any]) -> None:
        db = self._load()
        db["data"][str(user_id)] = data
        self._save(db)

class RedisStorage:
    """Enterprise Redis storage driver for high-load cluster deployments."""
    def __init__(self, redis_client: Any):
        self.redis = redis_client

    async def get_state(self, user_id: int) -> Optional[str]:
        val = await self.redis.get(f"navix:state:{user_id}")
        return val.decode("utf-8") if val else None

    async def set_state(self, user_id: int, state: Optional[str]) -> None:
        key = f"navix:state:{user_id}"
        if state is None:
            await self.redis.delete(key)
        else:
            await self.redis.set(key, state)

    async def get_data(self, user_id: int) -> Dict[str, Any]:
        val = await self.redis.get(f"navix:data:{user_id}")
        return json.loads(val.decode("utf-8")) if val else {}

    async def set_data(self, user_id: int, data: Dict[str, Any]) -> None:
        key = f"navix:data:{user_id}"
        await self.redis.set(key, json.dumps(data))

class State:
    def __init__(self, name: str):
        self.name = name

class StatesGroup:
    def __init_subclass__(cls, **kwargs):
        for key, value in cls.__dict__.items():
            if isinstance(value, State):
                value.name = f"{cls.__name__}:{key}"
