import time
from typing import Any, Dict, List

class TelemetryCollector:
    """Enterprise Metrics & Telemetry tracker for production health monitoring."""
    def __init__(self):
        self.total_requests = 0
        self.total_errors = 0
        self.handler_latencies: List[float] = []

    def record_request(self) -> None:
        self.total_requests += 1

    def record_error(self) -> None:
        self.total_errors += 1

    def record_latency(self, duration: float) -> None:
        self.handler_latencies.append(duration)

    def get_metrics_summary(self) -> Dict[str, Any]:
        avg_latency = sum(self.handler_latencies) / len(self.handler_latencies) if self.handler_latencies else 0.0
        return {
            "total_requests": self.total_requests,
            "total_errors": self.total_errors,
            "average_latency_seconds": round(avg_latency, 4)
        }
