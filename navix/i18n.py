from typing import Any, Dict, Optional

class I18n:
    """Enterprise Internationalization (i18n) manager for multi-language bots."""
    def __init__(self, default_locale: str = "fa"):
        self.default_locale = default_locale
        self.translations: Dict[str, Dict[str, str]] = {}

    def load_locales(self, locales_dict: Dict[str, Dict[str, str]]) -> None:
        self.translations = locales_dict

    def get(self, key: str, locale: Optional[str] = None, **kwargs: Any) -> str:
        loc = locale or self.default_locale
        text = self.translations.get(loc, {}).get(key, key)
        if kwargs:
            try:
                return text.format(**kwargs)
            except Exception:
                return text
        return text
