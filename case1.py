#!/usr/bin/env python

from lib.utc_bot import UTCBot, start_bot
import lib.proto.utc_bot as pb
import betterproto as bp
import math
import pprint as pp
import matplotlib.pyplot as mpl
import collections as co

import asyncio
import random

"""Constant listed from case packet"""
DAYS_IN_YEAR = 252
LAST_RATE_ROR_USD = 0.25
LAST_RATE_HAP_USD = 0.5
LAST_RATE_HAP_ROR = 2
TICK_SIZES = {
    "6RH": 0.00001,
    "6RM": 0.00001,
    "6RU": 0.00001,
    "6RZ": 0.00001,
    "6HH": 0.00002,
    "6HM": 0.00002,
    "6HU": 0.00002,
    "6HZ": 0.00002,
    "RHH": 0.0001,
    "RHM": 0.0001,
    "RHU": 0.0001,
    "RHZ": 0.0001,
    "RORUSD": 0.00001,
}
FUTURES = [i + j for i in ["6R", "6H", "RH"] for j in ["H", "M", "U", "Z"]]


def daily_rate(daily_rate):
    return math.pow(daily_rate, 1 / 252)


class PositionTrackerBot(UTCBot):
    async def handle_round_started(self):
        self.last = 0
        self.rate_points = []
        self.spot_points = co.defaultdict(list)

    async def handle_exchange_update(self, update: pb.FeedMessage):
        pass

if __name__ == "__main__":
    start_bot(PositionTrackerBot)
