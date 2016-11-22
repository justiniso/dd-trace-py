"""
a script which uses our integratiosn and prints memory statistics.
a very coarsely grained way of seeing how things are used.
"""


# stdlib
import itertools
import logging
import time
import sys

# 3p
import pympler.tracker
import redis

# project
import ddtrace
from tests.contrib import config


ddtrace.patch(redis=True)
ddtrace.tracer.writer = None


class KitchenSink(object):

    def __init__(self):
        self._redis = redis.Redis(**config.REDIS_CONFIG)

    def ping(self, i):
        self._ping_redis(i)

    def _ping_redis(self, i):
        with self._redis.pipeline() as p:
            p.get("a")
        self._redis.set("a", "b")
        self._redis.get("a")


if __name__ == '__main__':
    k = KitchenSink()
    t = pympler.tracker.SummaryTracker()
    for i in itertools.count():
        # do the work
        k.ping(i)

        # periodically print stats
        if i % 500 == 0:
            t.print_diff()
        time.sleep(0.0001)