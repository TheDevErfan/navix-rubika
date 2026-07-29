"""Navix Rubika Framework - Main Client."""

class NavixBot:
    """Main bot client for interacting with Rubika."""
    def __init__(self, token: str = None, **kwargs):
        self.token = token
        self.options = kwargs

    async def import_session(self) -> None:
        """Import or initialize bot session."""
        pass

    async def start(self) -> None:
        """Start the bot polling/webhook loop."""
        pass
