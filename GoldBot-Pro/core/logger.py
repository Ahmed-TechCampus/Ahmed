from pathlib import Path
from loguru import logger
import sys

# إنشاء مجلد السجلات تلقائياً
Path("logs").mkdir(exist_ok=True)

logger.remove()

# Console Logger
logger.add(
    sys.stdout,
    level="INFO",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)

# General Log
logger.add(
    "logs/system.log",
    rotation="10 MB",
    retention="30 days",
    level="INFO",
    encoding="utf-8"
)

# Error Log
logger.add(
    "logs/error.log",
    rotation="10 MB",
    retention="60 days",
    level="ERROR",
    encoding="utf-8"
)

# Trade Log
logger.add(
    "logs/trades.log",
    rotation="10 MB",
    retention="90 days",
    level="INFO",
    filter=lambda record: record["extra"].get("trade", False),
    encoding="utf-8"
)

trade_logger = logger.bind(trade=True)
