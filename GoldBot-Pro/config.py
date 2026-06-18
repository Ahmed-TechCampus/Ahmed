
from dotenv import load_dotenv
from pydantic import BaseModel
import os

load_dotenv()


class Settings(BaseModel):
    mt5_login: int
    mt5_password: str
    mt5_server: str

    symbol: str = "XAUUSD"

    timeframe: str = "M15"

    risk_percent: float = 1.0

    max_daily_trades: int = 3

    max_daily_loss: float = 3.0

    max_daily_profit: float = 6.0

    magic_number: int = 20260618


settings = Settings(
    mt5_login=int(os.getenv("MT5_LOGIN")),
    mt5_password=os.getenv("MT5_PASSWORD"),
    mt5_server=os.getenv("MT5_SERVER"),

    symbol=os.getenv("SYMBOL", "XAUUSD"),

    timeframe=os.getenv("TIMEFRAME", "M15"),

    risk_percent=float(os.getenv("RISK_PERCENT", 1.0)),

    max_daily_trades=int(os.getenv("MAX_DAILY_TRADES", 3)),

    max_daily_loss=float(os.getenv("MAX_DAILY_LOSS", 3.0)),

    max_daily_profit=float(os.getenv("MAX_DAILY_PROFIT", 6.0)),

    magic_number=int(os.getenv("MAGIC_NUMBER", 20260618))
)
