"""Tests for KorbitExchangeData container."""

from __future__ import annotations

from bt_api_korbit.exchange_data import KorbitExchangeData


class TestKorbitExchangeData:
    """Tests for KorbitExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = KorbitExchangeData()

        assert exchange.exchange_name == "KORBIT___SPOT"
