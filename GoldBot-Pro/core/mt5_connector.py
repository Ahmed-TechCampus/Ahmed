# core/mt5_connector.py

from __future__ import annotations

import MetaTrader5 as mt5
import pandas as pd

from config import settings
from core.logger import logger


class MT5Connector:

    def __init__(self):
        self.connected = False

    # ==========================
    # Connection Management
    # ==========================

    def connect(self) -> bool:

        if self.connected:
            return True

        if not mt5.initialize():

            logger.error(
                f"MT5 Initialize Failed: {mt5.last_error()}"
            )

            return False

        authorized = mt5.login(
            login=settings.mt5_login,
            password=settings.mt5_password,
            server=settings.mt5_server
        )

        if not authorized:

            logger.error(
                f"Login Failed: {mt5.last_error()}"
            )

            mt5.shutdown()

            return False

        self.connected = True

        logger.info("Connected To MT5")

        return True

    def disconnect(self):

        mt5.shutdown()

        self.connected = False

        logger.info("Disconnected From MT5")

    def reconnect(self) -> bool:

        logger.warning("Reconnecting To MT5")

        self.disconnect()

        return self.connect()

    # ==========================
    # Account
    # ==========================

    def account_info(self) -> dict | None:

        info = mt5.account_info()

        if info is None:

            logger.error("Unable To Get Account Info")

            return None

        return info._asdict()

    # ==========================
    # Symbol
    # ==========================

    def symbol_info(self, symbol: str):

        info = mt5.symbol_info(symbol)

        if info is None:

            logger.error(
                f"Symbol Not Found: {symbol}"
            )

            return None

        return info

    def get_tick(self, symbol: str):

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:

            logger.error(
                f"Tick Data Not Found: {symbol}"
            )

            return None

        return tick

    # ==========================
    # Market Data
    # ==========================

    def get_rates(
        self,
        symbol: str,
        timeframe,
        bars: int = 500
    ) -> pd.DataFrame:

        rates = mt5.copy_rates_from_pos(
            symbol,
            timeframe,
            0,
            bars
        )

        if rates is None:

            logger.error(
                f"Unable To Load Rates: {symbol}"
            )

            return pd.DataFrame()

        df = pd.DataFrame(rates)

        df["time"] = pd.to_datetime(
            df["time"],
            unit="s"
        )

        return df

    # ==========================
    # Positions
    # ==========================

    def positions(self, symbol: str | None = None):

        if symbol:

            return mt5.positions_get(
                symbol=symbol
            )

        return mt5.positions_get()

    # ==========================
    # Send Order
    # ==========================

    def send_order(
        self,
        symbol: str,
        order_type: int,
        volume: float,
        sl: float,
        tp: float,
        comment: str = "GoldBot"
    ):

        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            return None

        price = (
            tick.ask
            if order_type == mt5.ORDER_TYPE_BUY
            else tick.bid
        )

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "volume": volume,
            "type": order_type,
            "price": price,
            "sl": sl,
            "tp": tp,
            "deviation": 20,
            "magic": settings.magic_number,
            "comment": comment,
            "type_time": mt5.ORDER_TIME_GTC,
            "type_filling": mt5.ORDER_FILLING_IOC
        }

        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:

            logger.error(
                f"Order Failed: {result.retcode}"
            )

            return None

        logger.info(
            f"Order Executed | Ticket={result.order}"
        )

        return result

    # ==========================
    # Close Position
    # ==========================

    def close_position(
        self,
        ticket: int
    ):

        positions = mt5.positions_get(
            ticket=ticket
        )

        if not positions:

            logger.error(
                f"Position Not Found: {ticket}"
            )

            return False

        position = positions[0]

        tick = mt5.symbol_info_tick(
            position.symbol
        )

        close_type = (
            mt5.ORDER_TYPE_SELL
            if position.type == mt5.POSITION_TYPE_BUY
            else mt5.ORDER_TYPE_BUY
        )

        price = (
            tick.bid
            if position.type == mt5.POSITION_TYPE_BUY
            else tick.ask
        )

        request = {
            "action": mt5.TRADE_ACTION_DEAL,
            "position": position.ticket,
            "symbol": position.symbol,
            "volume": position.volume,
            "type": close_type,
            "price": price,
            "deviation": 20,
            "magic": settings.magic_number,
            "comment": "GoldBot Close"
        }

        result = mt5.order_send(request)

        if result.retcode != mt5.TRADE_RETCODE_DONE:

            logger.error(
                f"Close Failed: {result.retcode}"
            )

            return False

        logger.info(
            f"Position Closed | Ticket={ticket}"
        )

        return True
