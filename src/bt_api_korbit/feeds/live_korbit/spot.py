from __future__ import annotations

from typing import Any, Optional

from bt_api_korbit.feeds.live_korbit.request_base import KorbitRequestData


class KorbitRequestDataSpot(KorbitRequestData):
    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)

    def get_tick(self, symbol: str, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path, params, extra = self._get_tick(symbol, extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_tick(
        self, symbol: str, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any
    ):
        path, params, extra = self._get_tick(symbol, extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def _get_tick(self, symbol: str, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path = self._params.get_rest_path("get_tick")
        request_symbol = self._params.get_symbol(symbol)
        params = {"currency_pair": request_symbol}
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_tick",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_tick_normalize_function,
            }
        )
        return path, params, extra_data

    @staticmethod
    def _get_tick_normalize_function(input_data: Any, extra_data: Any):
        if KorbitRequestData._is_error(input_data):
            return [], False
        if isinstance(input_data, dict) and input_data:
            return [input_data], True
        return [], False

    def get_depth(self, symbol: str, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path, params, extra = self._get_depth(symbol, extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_depth(
        self, symbol: str, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any
    ):
        path, params, extra = self._get_depth(symbol, extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def _get_depth(self, symbol: str, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path = self._params.get_rest_path("get_depth")
        request_symbol = self._params.get_symbol(symbol)
        params = {"currency_pair": request_symbol}
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_depth",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_depth_normalize_function,
            }
        )
        return path, params, extra_data

    @staticmethod
    def _get_depth_normalize_function(input_data: Any, extra_data: Any):
        if KorbitRequestData._is_error(input_data):
            return [], False
        if isinstance(input_data, dict) and input_data:
            return [input_data], True
        return [], False

    def get_exchange_info(self, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path, params, extra = self._get_exchange_info(extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_exchange_info(
        self, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any
    ):
        path, params, extra = self._get_exchange_info(extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def _get_exchange_info(self, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path = self._params.get_rest_path("get_exchange_info")
        params: dict[str, Any] = {}
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_exchange_info",
                "symbol_name": None,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_exchange_info_normalize_function,
            }
        )
        return path, params, extra_data

    @staticmethod
    def _get_exchange_info_normalize_function(input_data: Any, extra_data: Any):
        if KorbitRequestData._is_error(input_data):
            return [], False
        if isinstance(input_data, list):
            return [input_data], True
        if isinstance(input_data, dict) and input_data:
            return [input_data], True
        return [], False

    def get_kline(
        self,
        symbol: str,
        period: str = "1h",
        count: int = 100,
        extra_data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ):
        path, params, extra = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_kline(
        self,
        symbol: str,
        period: str = "1h",
        count: int = 100,
        extra_data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ):
        path, params, extra = self._get_kline(symbol, period, count, extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def _get_kline(
        self,
        symbol: str,
        period: str = "1h",
        count: int = 100,
        extra_data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ):
        path = self._params.get_rest_path("get_kline")
        request_symbol = self._params.get_symbol(symbol)
        exchange_period = self._params.get_period(period)
        params: dict[str, Any] = {"currency_pair": request_symbol}
        if exchange_period:
            params["timeUnit"] = exchange_period
        if count:
            params["count"] = count
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_kline",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_kline_normalize_function,
            }
        )
        return path, params, extra_data

    @staticmethod
    def _get_kline_normalize_function(input_data: Any, extra_data: Any):
        if KorbitRequestData._is_error(input_data):
            return [], False
        if isinstance(input_data, list):
            return input_data, True
        if isinstance(input_data, dict) and input_data:
            return [input_data], True
        return [], False

    def make_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        amount: Any,
        price: Any = None,
        extra_data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ):
        path, body, extra = self._make_order(
            symbol, side, order_type, amount, price, extra_data, **kwargs
        )
        return self.request(path, body=body, extra_data=extra)

    async def async_make_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        amount: Any,
        price: Any = None,
        extra_data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ):
        path, body, extra = self._make_order(
            symbol, side, order_type, amount, price, extra_data, **kwargs
        )
        return await self.async_request(path, body=body, extra_data=extra)

    def _make_order(
        self,
        symbol: str,
        side: str,
        order_type: str,
        amount: Any,
        price: Any = None,
        extra_data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ):
        request_symbol = self._params.get_symbol(symbol)
        if side.lower() == "sell":
            path = self._params.get_rest_path("make_order_sell")
        else:
            path = self._params.get_rest_path("make_order")
        body = {
            "currency_pair": request_symbol,
            "type": order_type,
            "coin_amount": amount,
        }
        if price is not None and "limit" in order_type.lower():
            body["price"] = price
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "make_order",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._make_order_normalize_function,
            }
        )
        return path, body, extra_data

    @staticmethod
    def _make_order_normalize_function(input_data: Any, extra_data: Any):
        if KorbitRequestData._is_error(input_data):
            return [], False
        if isinstance(input_data, dict) and input_data:
            return [input_data], True
        return [], False

    def cancel_order(
        self, order_id: Any, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any
    ):
        path, body, extra = self._cancel_order(order_id, extra_data, **kwargs)
        return self.request(path, body=body, extra_data=extra)

    async def async_cancel_order(
        self, order_id: Any, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any
    ):
        path, body, extra = self._cancel_order(order_id, extra_data, **kwargs)
        return await self.async_request(path, body=body, extra_data=extra)

    def _cancel_order(
        self, order_id: Any, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any
    ):
        path = self._params.get_rest_path("cancel_order")
        body = {
            "id": order_id,
            "currency_pair": kwargs.get("currency_pair", "btc_krw"),
        }
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "cancel_order",
                "symbol_name": None,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._cancel_order_normalize_function,
            }
        )
        return path, body, extra_data

    @staticmethod
    def _cancel_order_normalize_function(input_data: Any, extra_data: Any):
        if KorbitRequestData._is_error(input_data):
            return [], False
        if isinstance(input_data, dict) and input_data:
            return [input_data], True
        return [{}], True

    def get_open_orders(
        self,
        symbol: Optional[str] = None,
        extra_data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ):
        path, params, extra = self._get_open_orders(symbol, extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_open_orders(
        self,
        symbol: Optional[str] = None,
        extra_data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ):
        path, params, extra = self._get_open_orders(symbol, extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def _get_open_orders(
        self,
        symbol: Optional[str] = None,
        extra_data: Optional[dict[str, Any]] = None,
        **kwargs: Any,
    ):
        path = self._params.get_rest_path("get_open_orders")
        params: dict[str, Any] = {}
        if symbol:
            params["currency_pair"] = self._params.get_symbol(symbol)
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_open_orders",
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_open_orders_normalize_function,
            }
        )
        return path, params, extra_data

    @staticmethod
    def _get_open_orders_normalize_function(input_data: Any, extra_data: Any):
        if KorbitRequestData._is_error(input_data):
            return [], False
        if isinstance(input_data, list):
            return input_data, True
        if isinstance(input_data, dict) and input_data:
            return [input_data], True
        return [], False

    def get_balance(self, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path, params, extra = self._get_balance(extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_balance(self, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path, params, extra = self._get_balance(extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def _get_balance(self, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path = self._params.get_rest_path("get_balance")
        params: dict[str, Any] = {}
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_balance",
                "symbol_name": None,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_balance_normalize_function,
            }
        )
        return path, params, extra_data

    @staticmethod
    def _get_balance_normalize_function(input_data: Any, extra_data: Any):
        if KorbitRequestData._is_error(input_data):
            return [], False
        if isinstance(input_data, dict) and input_data:
            return [input_data], True
        if isinstance(input_data, list):
            return input_data, True
        return [], False

    def get_account(self, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path, params, extra = self._get_account(extra_data, **kwargs)
        return self.request(path, params, extra_data=extra)

    async def async_get_account(self, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path, params, extra = self._get_account(extra_data, **kwargs)
        return await self.async_request(path, params, extra_data=extra)

    def _get_account(self, extra_data: Optional[dict[str, Any]] = None, **kwargs: Any):
        path = self._params.get_rest_path("get_account")
        params: dict[str, Any] = {}
        extra_data = extra_data or {}
        extra_data.update(
            {
                "request_type": "get_account",
                "symbol_name": None,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_account_normalize_function,
            }
        )
        return path, params, extra_data

    @staticmethod
    def _get_account_normalize_function(input_data: Any, extra_data: Any):
        if KorbitRequestData._is_error(input_data):
            return [], False
        if isinstance(input_data, dict) and input_data:
            return [input_data], True
        if isinstance(input_data, list):
            return input_data, True
        return [], False
