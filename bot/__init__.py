"""
Trading Bot Package.
"""

from bot.client import BinanceClient
from bot.orders import place_market_order, place_limit_order
from bot.exceptions import TradingBotError, ValidationError, BinanceAPIError, NetworkError
from bot.validators import validate_order_params
from bot.logging_config import setup_logging
from bot.utils import (
    print_success,
    print_error,
    print_info,
    print_warning,
    ask_confirmation,
    print_order_request,
    print_order_response,
)

__all__ = [
    "BinanceClient",
    "place_market_order",
    "place_limit_order",
    "TradingBotError",
    "ValidationError",
    "BinanceAPIError",
    "NetworkError",
    "validate_order_params",
    "setup_logging",
    "print_success",
    "print_error",
    "print_info",
    "print_warning",
    "ask_confirmation",
    "print_order_request",
    "print_order_response",
]
