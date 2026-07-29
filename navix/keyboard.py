"""
Modern Keyboard Builder for Navix Framework
"""

class InlineKeyboardBuilder:
    """سازنده پیشرفته و زنجیره‌ای کیبوردهای شیشه‌ای برای روبیکا"""
    def __init__(self):
        self.rows = []
        self.current_row = []

    def add(self, text: str, callback_data: str = None, url: str = None):
        button = {"text": text}
        if callback_data:
            button["callback_data"] = callback_data
        if url:
            button["url"] = url
        self.current_row.append(button)
        return self

    def row(self):
        if self.current_row:
            self.rows.append(self.current_row)
            self.current_row = []
        return self

    def adjust(self, *sizes):
        flat_buttons = [btn for row in self.rows for btn in row] + self.current_row
        self.rows = []
        self.current_row = []
        
        index = 0
        for size in sizes:
            row = flat_buttons[index:index + size]
            if row:
                self.rows.append(row)
            index += size
        
        if index < len(flat_buttons):
            self.rows.append(flat_buttons[index:])
        return self

    def export(self) -> list:
        if self.current_row:
            self.rows.append(self.current_row)
            self.current_row = []
        return self.rows
