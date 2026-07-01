"""
Order placement business logic.
Provides high-level, reusable order functions.
"""

from typing import Any
from bot.client import BinanceClient


def place_market_order(
    client: BinanceClient, symbol: str, side: str, quantity: float
) -> dict[str, Any]:
    """
    Places a Market Order on the USDT-M Futures Testnet.
    
    Receives validated data only.
    """
    return client.execute_futures_order(
        symbol=symbol,
        side=side,
        order_type="MARKET",
        quantity=quantity,
        price=None
    )


def place_limit_order(
    client: BinanceClient, symbol: str, side: str, quantity: float, price: float
) -> dict[str, Any]:
    """
    Places a Limit Order on the USDT-M Futures Testnet.
    
    Receives validated data only.
    """
    return client.execute_futures_order(
        symbol=symbol,
        side=side,
        order_type="LIMIT",
        quantity=quantity,
        price=price
    )
