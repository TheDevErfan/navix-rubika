import asyncio
import logging
from typing import Callable, Any

logger = logging.getLogger("navix")

class BackgroundTasks:
    """Enterprise background task runner for non-blocking asynchronous operations."""
    def __init__(self):
        self.tasks = set()

    def add_task(self, func: Callable, *args: Any, **kwargs: Any) -> None:
        """Schedules a background task to run concurrently without blocking handlers."""
        if asyncio.iscoroutinefunction(func):
            task = asyncio.create_task(func(*args, **kwargs))
        else:
            loop = asyncio.get_running_loop()
            task = loop.run_in_executor(None, lambda: func(*args, **kwargs))
        
        self.tasks.add(task)
        task.add_done_callback(self.tasks.discard)
