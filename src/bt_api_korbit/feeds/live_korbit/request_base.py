from __future__ import annotations

from typing import Any, Optional
from urllib.parse import urlencode

from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.logging_factory import get_logger

from bt_api_korbit.exchange_data import KorbitExchangeDataSpot


class KorbitRequestData(Feed):
    @classmethod
    def _capabilities(cls) -> set[Capability]:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_DEALS,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.QUERY_OPEN_ORDERS,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.data_queue = data_queue
        self.api_key = kwargs.get("public_key") or kwargs.get("api_key") or ""
        self._api_secret = kwargs.get("private_key") or kwargs.get("api_secret") or ""
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self.exchange_name = kwargs.get("exchange_name", "KORBIT___SPOT")
        self._params = KorbitExchangeDataSpot()
        self.request_logger = get_logger("korbit_spot_feed")
        self.async_logger = get_logger("korbit_spot_feed")

    def _get_headers(self) -> dict[str, str]:
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        return headers

    def push_data_to_queue(self, data: Any) -> None:
        if self.data_queue is not None:
            self.data_queue.put(data)

    def request(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
        body: Any = None,
        extra_data: Optional[dict[str, Any]] = None,
        timeout: int = 10,
    ) -> RequestData:
        if params is None:
            params = {}
        method, endpoint = path.split(" ", 1)
        headers = self._get_headers()

        if method == "GET":
            qs = urlencode(params) if params else ""
            url = f"{self._params.rest_url}{endpoint}{'?' + qs if qs else ''}"
            json_body = None
        else:
            url = f"{self._params.rest_url}{endpoint}"
            json_body = body if body is not None else params
            if not json_body:
                json_body = None

        res = self.http_request(method, url, headers, json_body, timeout)
        return RequestData(res, extra_data)

    async def async_request(
        self,
        path: str,
        params: Optional[dict[str, Any]] = None,
        body: Any = None,
        extra_data: Optional[dict[str, Any]] = None,
        timeout: int = 5,
    ) -> RequestData:
        if params is None:
            params = {}
        method, endpoint = path.split(" ", 1)
        headers = self._get_headers()

        if method == "GET":
            qs = urlencode(params) if params else ""
            url = f"{self._params.rest_url}{endpoint}{'?' + qs if qs else ''}"
            json_body = None
        else:
            url = f"{self._params.rest_url}{endpoint}"
            json_body = body if body is not None else params
            if not json_body:
                json_body = None

        res = await self.async_http_request(method, url, headers, json_body, timeout)
        return RequestData(res, extra_data)

    def async_callback(self, request_data: Any) -> None:
        if request_data is not None:
            self.push_data_to_queue(request_data)

    @staticmethod
    def _is_error(input_data: Any) -> bool:
        if input_data is None:
            return True
        return bool(isinstance(input_data, dict) and "errorCode" in input_data)
