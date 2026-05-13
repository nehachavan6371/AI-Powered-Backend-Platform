"""Monitoring and Metrics"""

import logging
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class PerformanceMonitor:
    """Monitor application performance"""

    def __init__(self):
        """Initialize monitor"""
        self.metrics = defaultdict(list)

    def record_metric(self, metric_name: str, value: float):
        """Record a metric"""
        self.metrics[metric_name].append({
            "value": value,
            "timestamp": datetime.utcnow()
        })

    def get_average(self, metric_name: str) -> float:
        """Get average value for metric"""
        values = [m["value"] for m in self.metrics.get(metric_name, [])]
        if not values:
            return 0.0
        return sum(values) / len(values)

    def get_stats(self, metric_name: str) -> dict:
        """Get statistics for metric"""
        values = [m["value"] for m in self.metrics.get(metric_name, [])]
        if not values:
            return {}
        
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values)
        }
