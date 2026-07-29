import re
import time

class TextFormatter:
    @staticmethod
    def format(text):
        return text

    @staticmethod
    def slugify(text):
        text = text.lower()
        text = re.sub(r'[^a-z0-9\s-]', '', text)
        text = re.sub(r'[\s_-]+', '-', text).strip('-')
        return text

class Validators:
    @staticmethod
    def validate(val):
        return True

    @staticmethod
    def is_email(email):
        return bool(re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", email))

class TTLCache:
    def __init__(self, ttl=300):
        self.ttl = ttl
        self.store = {}

    def set(self, key, value):
        self.store[key] = (value, time.time() + self.ttl)

    def get(self, key, default=None):
        if key in self.store:
            val, expiry = self.store[key]
            if time.time() < expiry:
                return val
            else:
                del self.store[key]
        return default
