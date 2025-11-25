"""
Small in-memory metrics logger. In production push to Prometheus/Cloud Monitoring.
"""
import time
import logging
logger = logging.getLogger("metrics")

class MetricsLogger:
    def __init__(self):
        self.counter = {}
        self.timers = {}

    def inc(self, key, amount=1):
        self.counter[key] = self.counter.get(key, 0) + amount

    def timing(self, key, seconds):
        self.timers[key] = seconds

    def snapshot(self):
        return {"counters": self.counter.copy(), "timers": self.timers.copy()}
