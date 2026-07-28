from typing import Callable, List, Tuple, Optional, Any

class Router:
    """Router for organizing message handlers, callback handlers, and sub-routers."""
    def __init__(self):
        self.message_handlers: List[Tuple[tuple, Callable]] = []
        self.callback_handlers: List[Tuple[Optional[str], Callable]] = []
        self.sub_routers: List['Router'] = []
        self.middlewares: List[Any] = []

    def include_router(self, router: 'Router') -> None:
        """Includes a sub-router."""
        self.sub_routers.append(router)

    def middleware(self, middleware_cls: Any) -> None:
        """Registers a middleware instance."""
        self.middlewares.append(middleware_cls)

    def message(self, *filters: Callable) -> Callable:
        """Decorator to register message handlers with filters."""
        def decorator(handler: Callable) -> Callable:
            self.message_handlers.append((filters, handler))
            return handler
        return decorator

    def callback_query(self, pattern: Optional[str] = None) -> Callable:
        """Decorator to register callback query handlers."""
        def decorator(handler: Callable) -> Callable:
            self.callback_handlers.append((pattern, handler))
            return handler
        return decorator
