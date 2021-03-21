#!/usr/bin/env python

from utc_bot import UTCBot, start_bot
import proto.utc_bot as pb
import betterproto as bp
import math
import re
import pprint as pp
import matplotlib.pyplot as mpl
import collections as co

import asyncio
import random

from typing import Optional

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


def round_nearest(x, tick=0.0001):
    """Rounds price to nearest tick_number above"""
    return round(round(x / tick) * tick, -int(math.floor(math.log10(tick))))


def daily_rate(daily_rate):
    """Finds daily interest rates from annual rate"""
    return math.pow(daily_rate, 1 / 252)


class PositionTrackerBot(UTCBot):
    async def handle_round_started(self):
        self.last = 0
        self.rate_points = []
        self.spot_points = co.defaultdict(list)

    async def handle_exchange_update(self, update: pb.FeedMessage):
        name, value = bp.which_one_of(update, "msg")

        if name == "generic_msg" and value.event_type == pb.GenericMessageType.MESSAGE:
            parts = value.message.split(", ")
            if len(parts) != 4:
                return

            ror, hap, usd = map(float, parts[1:])
            self.rate_points.append((self.last, [ror, hap, usd]))

        if name == "market_snapshot_msg":
            self.last = float(value.timestamp.split("=+")[-1])
            for asset, book in value.books.items():
                if not book.bids or not book.asks:
                    continue
                self.spot_points[asset].append(
                    (self.last, [float(book.bids[0].px), float(book.asks[0].px)])
                )

        if self.last > 240:
            self.show_plot()

    def show_plot(self):
        fig, [ax_rates, *ax_spots] = mpl.subplots(1 + len(self.spot_points))
        plot_points(ax_rates, self.rate_points, ["ror", "hap", "usd"])
        ax_rates.set_ylabel("interest")
        for ax, (asset, pts) in zip(ax_spots, self.spot_points.items()):
            ax.set_ylabel(asset)
            plot_points(ax, pts, ["bid", "ask"])
        mpl.tight_layout()
        mpl.show()


def plot_points(ax, pts, labels):
    xs, ys = [*zip(*pts)]
    ax.legend(ax.plot(xs, ys), labels)


if __name__ == "__main__":
    start_bot(PositionTrackerBot)


# FeedMessage(
#    request_failed_msg=RequestFailedMessage(
#        type=0,
#        place_order_id="",
#        cancel_order_id="",
#        message="",
#        asset="",
#        timestamp="",
#    ),
#    pnl_msg=PnLMessage(realized_pnl="", m2m_pnl="", timestamp=""),
#    trade_msg=TradeMessage(asset="", price="", qty=0, timestamp=""),
#    fill_msg=FillMessage(
#        order_id="",
#        asset="",
#        order_side=0,
#        price="",
#        filled_qty=0,
#        remaining_qty=0,
#        timestamp="",
#    ),
#    market_snapshot_msg=MarketSnapshotMessage(
#        books={
#            "6HH": MarketSnapshotMessageBook(
#                asset="6HH",
#                bids=[
#                    MarketSnapshotMessageBookPriceLevel(px="0.49998", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.49996", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.49994", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.49992", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.4999", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.49988", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.49986", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.49984", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.49982", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.4998", qty=2000),
#                ],
#                asks=[
#                    MarketSnapshotMessageBookPriceLevel(px="0.50002", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.50004", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.50006", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.50008", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.5001", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.50012", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.50014", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.50016", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.50018", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.5002", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="4.995", qty=10),
#                    MarketSnapshotMessageBookPriceLevel(px="4.99502", qty=10),
#                ],
#            ),
#            "6RM": MarketSnapshotMessageBook(asset="6RM", bids=[], asks=[]),
#            "6RZ": MarketSnapshotMessageBook(asset="6RZ", bids=[], asks=[]),
#            "RHH": MarketSnapshotMessageBook(
#                asset="RHH",
#                bids=[
#                    MarketSnapshotMessageBookPriceLevel(px="1.9999", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="1.9998", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="1.9997", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="1.9996", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="1.9995", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="1.9994", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="1.9993", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="1.9992", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="1.9991", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="1.999", qty=2000),
#                ],
#                asks=[
#                    MarketSnapshotMessageBookPriceLevel(px="2.0001", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="2.0002", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="2.0003", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="2.0004", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="2.0005", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="2.0006", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="2.0007", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="2.0008", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="2.0009", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="2.001", qty=2000),
#                ],
#            ),
#            "6HZ": MarketSnapshotMessageBook(asset="6HZ", bids=[], asks=[]),
#            "RHU": MarketSnapshotMessageBook(asset="RHU", bids=[], asks=[]),
#            "6HU": MarketSnapshotMessageBook(asset="6HU", bids=[], asks=[]),
#            "RHM": MarketSnapshotMessageBook(asset="RHM", bids=[], asks=[]),
#            "6RU": MarketSnapshotMessageBook(asset="6RU", bids=[], asks=[]),
#            "RORUSD": MarketSnapshotMessageBook(
#                asset="RORUSD",
#                bids=[
#                    MarketSnapshotMessageBookPriceLevel(px="0.2557", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25569", qty=2800),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25568", qty=3600),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25567", qty=4400),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25565", qty=5200),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25564", qty=6000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25563", qty=6800),
#                ],
#                asks=[
#                    MarketSnapshotMessageBookPriceLevel(px="0.25573", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25574", qty=2800),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25575", qty=3600),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25577", qty=4400),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25578", qty=5200),
#                    MarketSnapshotMessageBookPriceLevel(px="0.2558", qty=6000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25581", qty=6800),
#                ],
#            ),
#            "6HM": MarketSnapshotMessageBook(asset="6HM", bids=[], asks=[]),
#            "RHZ": MarketSnapshotMessageBook(asset="RHZ", bids=[], asks=[]),
#            "6RH": MarketSnapshotMessageBook(
#                asset="6RH",
#                bids=[
#                    MarketSnapshotMessageBookPriceLevel(px="0.24999", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.24998", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.24997", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.24996", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.24995", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.24994", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.24993", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.24992", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.24991", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.2499", qty=2000),
#                ],
#                asks=[
#                    MarketSnapshotMessageBookPriceLevel(px="0.25001", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25002", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25003", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25004", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25005", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25006", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25007", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25008", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.25009", qty=2000),
#                    MarketSnapshotMessageBookPriceLevel(px="0.2501", qty=2000),
#                ],
#            ),
#        },
#        timestamp="2021-03-21 11:03:22.87753917 -0700 PDT m=+125.010045483",
#    ),
#    liquidation_msg=LiquidationMessage(message="", order_id="", asset="", timestamp=""),
#    generic_msg=GenericMessage(event_type=0, message=""),
# )
