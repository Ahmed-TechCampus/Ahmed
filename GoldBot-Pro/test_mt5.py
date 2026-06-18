import MetaTrader5 as mt5

from core.mt5_connector import MT5Connector

bot = MT5Connector()

if bot.connect():

    print("=" * 50)
    print("ACCOUNT INFO")
    print("=" * 50)

    print(bot.account_info())

    print("\n")

    print("=" * 50)
    print("XAUUSD DATA")
    print("=" * 50)

    df = bot.get_rates(
        "XAUUSD",
        mt5.TIMEFRAME_M15,
        10
    )

    print(df)

    print("\n")

    print("=" * 50)
    print("OPEN POSITIONS")
    print("=" * 50)

    print(bot.positions())

    bot.disconnect()
