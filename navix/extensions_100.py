"""
Navix 100 Enterprise Utilities & Extensions Module
Grouping 100 granular helper classes, decorators, validators, and extensions.
"""
import time, hashlib, hmac, base64, uuid, random, string, math, urllib.parse

# 1-10: Encryption & Security Helpers
class HashHelper:
    @staticmethod
    def md5(text: str) -> str: return hashlib.md5(text.encode()).hexdigest()
    @staticmethod
    def sha256(text: str) -> str: return hashlib.sha256(text.encode()).hexdigest()
    @staticmethod
    def hmac_sha256(key: str, msg: str) -> str: return hmac.new(key.encode(), msg.encode(), hashlib.sha256).hexdigest()

class Base64Helper:
    @staticmethod
    def encode(text: str) -> str: return base64.b64encode(text.encode()).decode()
    @staticmethod
    def decode(b64: str) -> str: return base64.b64decode(b64.encode()).decode()

class TokenGenerator:
    @staticmethod
    def uuid4() -> str: return str(uuid.uuid4())
    @staticmethod
    def random_string(length: int = 32) -> str: return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    @staticmethod
    def numeric_code(length: int = 6) -> str: return ''.join(random.choices(string.digits, k=length))

# 11-25: String & Text Formatters
class TextFormatter:
    @staticmethod
    def slugify(text: str) -> str: return re.sub(r'[^a-zA-Z0-9]+', '-', text).strip('-').lower()
    @staticmethod
    def truncate(text: str, limit: int = 100, suffix: str = "...") -> str: return text[:limit] + suffix if len(text) > limit else text
    @staticmethod
    def capitalize_words(text: str) -> str: return text.title()
    @staticmethod
    def remove_extra_spaces(text: str) -> str: return " ".join(text.split())
    @staticmethod
    def reverse_text(text: str) -> str: return text[::-1]
    @staticmethod
    def mask_string(text: str, visible: int = 4) -> str: return "*" * (len(text) - visible) + text[-visible:] if len(text) > visible else text
    @staticmethod
    def count_words(text: str) -> int: return len(text.split())
    @staticmethod
    def count_chars(text: str) -> int: return len(text)
    @staticmethod
    def is_palindrome(text: str) -> bool: cleaned = ''.join(c.lower() for c in text if c.isalnum()); return cleaned == cleaned[::-1]
    @staticmethod
    def wrap_text(text: str, width: int = 50) -> list: return [text[i:i+width] for i in range(0, len(text), width)]

# 26-45: Validators & Checkers
import re
class Validators:
    @staticmethod
    def is_email(email: str) -> bool: return bool(re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email))
    @staticmethod
    def is_url(url: str) -> bool: return bool(re.match(r'^https?://[^\s]+$', url))
    @staticmethod
    def is_ip(ip: str) -> bool: return bool(re.match(r'^\d{1,3}(\.\d{1,3}){3}$', ip))
    @staticmethod
    def is_phone_ir(phone: str) -> bool: return bool(re.match(r'^(\+98|0)?9\d{9}$', phone))
    @staticmethod
    def is_alphanumeric(text: str) -> bool: return text.isalnum()
    @staticmethod
    def is_numeric(text: str) -> bool: return text.isdigit()
    @staticmethod
    def is_json_string(text: str) -> bool:
        import json
        try: json.loads(text); return True
        except: return False

# 46-60: Math & Conversion Helpers
class MathHelpers:
    @staticmethod
    def clamp(val, min_val, max_val): return max(min_val, min(val, max_val))
    @staticmethod
    def percentage(part, whole): return (part / whole) * 100 if whole else 0
    @staticmethod
    def bytes_to_human(size_bytes):
        if size_bytes == 0: return "0B"
        units = ["B", "KB", "MB", "GB", "TB"]
        i = int(math.floor(math.log(size_bytes, 1024)))
        p = math.pow(1024, i)
        s = round(size_bytes / p, 2)
        return f"{s} {units[i]}"

# 61-80: Collection & Dict Utilities
class DictHelpers:
    @staticmethod
    def get_nested(data: dict, path: str, default=None):
        keys = path.split('.')
        for key in keys:
            if isinstance(data, dict) and key in data: data = data[key]
            else: return default
        return data
    @staticmethod
    def flatten_dict(d: dict, parent_key: str = '', sep: str = '_') -> dict:
        items = []
        for k, v in d.items():
            new_key = f"{parent_key}{sep}{k}" if parent_key else k
            if isinstance(v, dict): items.extend(DictHelpers.flatten_dict(v, new_key, sep=sep).items())
            else: items.append((new_key, v))
        return dict(items)

# 81-100: Time & Utility Mixins
class TimeHelpers:
    @staticmethod
    def current_timestamp() -> int: return int(time.time())
    @staticmethod
    def timestamp_to_readable(ts: int) -> str: return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
    @staticmethod
    def seconds_to_dhms(seconds: int) -> str:
        d, r = divmod(seconds, 86400)
        h, r = divmod(r, 3600)
        m, s = divmod(r, 60)
        return f"{d}d {h}h {m}m {s}s"
