from __future__ import annotations

from bt_api_base.containers.exchanges.exchange_data import ExchangeData


_FALLBACK_REST_PATHS = {
    "get_tick": "GET /v1/ticker/detailed",
    "get_depth": "GET /v1/orderbook",
    "get_deals": "GET /v1/transactions",
    "get_exchange_info": "GET /v1/constants",
    "get_kline": "GET /v1/chart/units",
    "make_order": "POST /v1/user/orders/buy",
    "make_order_sell": "POST /v1/user/orders/sell",
    "cancel_order": "POST /v1/user/orders/cancel",
    "get_open_orders": "GET /v1/user/orders/open",
    "get_balance": "GET /v1/user/balances",
    "get_account": "GET /v1/user/balances",
}


class KorbitExchangeData(ExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "KORBIT___SPOT"
        self.rest_url = "https://api.korbit.co.kr"
        self.wss_url = "wss://ws-api.korbit.co.kr/v2/public"
        self.rest_paths = dict(_FALLBACK_REST_PATHS)
        self.wss_paths = {}
        self.kline_periods = {
            "1m": "1m",
            "3m": "3m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "4h": "4h",
            "1d": "1d",
        }
        self.reverse_kline_periods = {v: k for k, v in self.kline_periods.items()}
        self.legal_currency = ["KRW", "BTC", "ETH"]


class KorbitExchangeDataSpot(KorbitExchangeData):
    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "SPOT"

    @staticmethod
    def get_symbol(symbol: str) -> str:
        return symbol.lower().replace("/", "_").replace("-", "_")

    @staticmethod
    def get_reverse_symbol(symbol: str) -> str:
        return symbol.upper().replace("_", "-")

    def get_period(self, key: str) -> str:
        return self.kline_periods.get(key, key)

    def get_reverse_period(self, key: str) -> str:
        return self.reverse_kline_periods.get(key, key)

    def get_rest_path(self, key: str, **kwargs) -> str:
        if key not in self.rest_paths or self.rest_paths[key] == "":
            raise ValueError(f"[{self.exchange_name}] REST path not found: {key}")
        return self.rest_paths[key]
