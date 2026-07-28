from typing import Any, List, Optional

class InlineKeyboardButton:
    def __init__(self, text: str, callback_data: Optional[str] = None, url: Optional[str] = None):
        self.text = text
        self.callback_data = callback_data
        self.url = url

    def to_dict(self) -> dict:
        d = {"text": self.text}
        if self.callback_data:
            d["callback_data"] = self.callback_data
        if self.url:
            d["url"] = self.url
        return d

class InlineKeyboardBuilder:
    def __init__(self):
        self.keyboard: List[List[dict]] = []
        self._current_row: List[dict] = []

    def add(self, *buttons: InlineKeyboardButton) -> 'InlineKeyboardBuilder':
        for btn in buttons:
            self._current_row.append(btn.to_dict())
        return self

    def row(self, *buttons: InlineKeyboardButton) -> 'InlineKeyboardBuilder':
        if self._current_row:
            self.keyboard.append(self._current_row)
            self._current_row = []
        self.keyboard.append([btn.to_dict() for btn in buttons])
        return self

    def adjust(self, *sizes: int) -> 'InlineKeyboardBuilder':
        all_buttons = [btn for row in self.keyboard for btn in row]
        if self._current_row:
            all_buttons.extend(self._current_row)
            self._current_row = []
        
        self.keyboard = []
        idx = 0
        for size in sizes:
            if idx >= len(all_buttons):
                break
            self.keyboard.append(all_buttons[idx:idx+size])
            idx += size
        
        while idx < len(all_buttons):
            self.keyboard.append(all_buttons[idx:idx+1])
            idx += 1
        return self

    def as_markup(self) -> dict:
        if self._current_row:
            self.keyboard.append(self._current_row)
            self._current_row = []
        return {"inline_keyboard": self.keyboard}

class Paginator:
    """Enterprise Paginator helper for clean inline keyboard pagination."""
    def __init__(self, items: List[Any], page: int = 1, per_page: int = 5, prefix: str = "page"):
        self.items = items
        self.page = page
        self.per_page = per_page
        self.prefix = prefix

    def get_page_items(self) -> List[Any]:
        start = (self.page - 1) * self.per_page
        end = start + self.per_page
        return self.items[start:end]

    def as_markup(self) -> dict:
        builder = InlineKeyboardBuilder()
        total_pages = (len(self.items) + self.per_page - 1) // self.per_page
        
        if total_pages > 1:
            row = []
            if self.page > 1:
                row.append(InlineKeyboardButton("⬅️ قبلی", callback_data=f"{self.prefix}:{self.page-1}"))
            row.append(InlineKeyboardButton(f"صفحه {self.page} از {total_pages}", callback_data="none"))
            if self.page < total_pages:
                row.append(InlineKeyboardButton("بعدی ➡️", callback_data=f"{self.prefix}:{self.page+1}"))
            builder.row(*row)
            
        return builder.as_markup()
