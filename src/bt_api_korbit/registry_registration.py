from __future__ import annotations

from typing import Any

from bt_api_base.balance_utils import nested_balance_handler as _korbit_balance_handler
from bt_api_base.registry import ExchangeRegistry

from bt_api_korbit.exchange_data import KorbitExchangeDataSpot
from bt_api_korbit.feeds.live_korbit.spot import KorbitRequestDataSpot


def _korbit_spot_subscribe_handler(data_queue: Any, exchange_params: Any, topics: Any, bt_api: Any) -> None:
    topic_list = [i["topic"] for i in topics]
    bt_api.log(f"Korbit Spot topics requested: {topic_list}")


def register_korbit(registry: type[ExchangeRegistry]) -> None:
    registry.register_feed("KORBIT___SPOT", KorbitRequestDataSpot)
    registry.register_exchange_data("KORBIT___SPOT", KorbitExchangeDataSpot)
    registry.register_balance_handler("KORBIT___SPOT", _korbit_balance_handler)
    registry.register_stream("KORBIT___SPOT", "subscribe", _korbit_spot_subscribe_handler)
