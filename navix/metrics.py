"""
Runtime Metrics and Performance Telemetry System for Navix
"""
import time
from typing import Dict, Any
from .log import logger

class MetricsCollector:
    """
    جمع‌آوری و پایش آنی متریک‌ها، آمار عملکرد، خطاها و تعداد درخواست‌های ربات
    """
    def __init__(self):
        self.start_time = time.time()
        self.total_requests = 0
        self.total_updates = 0
        self.total_errors = 0
        self.endpoint_stats: Dict[str, int] = {}
        self.error_stats: Dict[str, int] = {}
        logger.debug("سیستم متریک‌ها و تله‌متری (MetricsCollector) راه‌اندازی شد.")

    def record_request(self, method: str):
        self.total_requests += 1
        self.endpoint_stats[method] = self.endpoint_stats.get(method, 0) + 1

    def record_update(self):
        self.total_updates += 1

    def record_error(self, error_type: str):
        self.total_errors += 1
        self.error_stats[error_type] = self.error_stats.get(error_type, 0) + 1

    def get_uptime(self) -> float:
        return time.time() - self.start_time

    def get_summary(self) -> Dict[str, Any]:
        uptime = self.get_uptime()
        return {
            "uptime_seconds": round(uptime, 2),
            "total_requests": self.total_requests,
            "total_updates": self.total_updates,
            "total_errors": self.total_errors,
            "endpoint_breakdown": self.endpoint_stats,
            "error_breakdown": self.error_stats
        }

    def log_summary(self):
        summary = self.get_summary()
        logger.info(
            f"\n📊 [METRICS & TELEMETRY REPORT]\n"
            f"• مدت زمان اجرا (Uptime): {summary['uptime_seconds']} ثانیه\n"
            f"• کل درخواست‌های ارسالی به API: {summary['total_requests']}\n"
            f"• کل آپدیت‌های دریافتی: {summary['total_updates']}\n"
            f"• کل خطاهای ثبت‌شده: {summary['total_errors']}\n"
            f"• تفکیک درخواست‌های متدها: {summary['endpoint_breakdown']}\n"
            f"• تفکیک خطاها: {summary['error_breakdown']}\n"
            f"----------------------------------------"
        )

# ایجاد نمونه سراسری برای استفاده در سراسر کتابخانه
metrics = MetricsCollector()
