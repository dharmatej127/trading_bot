"""
Validation utilities for order parameters.
"""

import re
from bot.exceptions import ValidationError

# Regex to check standard symbol format (e.g. BTCUSDT, ETHUSDT)
SYMBOL_PATTERN = re.compile(r"^[A-Z0-9]{5,20}$")


def validate_symbol(symbol: str) -> None:
    """
    Validates that the trading symbol is uppercase alphanumeric and of a realistic length.
    
    Raises ValidationError if the symbol format is invalid.
    """
    if not symbol:
        raise ValidationError("Symbol is required and cannot be empty.")
    
    if not SYMBOL_PATTERN.match(symbol):
        raise ValidationError(
            f"Invalid symbol: '{symbol}'. Must be an uppercase alphanumeric string "
            f"of length 5 to 20 (e.g., 'BTCUSDT')."
        )


def validate_side(side: str) -> None:
    """
    Validates that the order side is either BUY or SELL.
    
    Raises ValidationError if the side is invalid.
    """
    if side not in ("BUY", "SELL"):
        raise ValidationError(f"Invalid side: '{side}'. Must be 'BUY' or 'SELL'.")


def validate_type(order_type: str) -> None:
    """
    Validates that the order type is either MARKET or LIMIT.
    
    Raises ValidationError if the order type is invalid.
    """
    if order_type not in ("MARKET", "LIMIT"):
        raise ValidationError(
            f"Invalid order type: '{order_type}'. Must be 'MARKET' or 'LIMIT'."
        )


def validate_quantity(quantity: float) -> None:
    """
    Validates that the quantity is greater than zero.
    
    Raises ValidationError if quantity is 0 or negative.
    """
    if quantity <= 0:
        raise ValidationError(f"Quantity must be greater than zero. Got {quantity}.")


def validate_price(price: float | None, order_type: str) -> None:
    """
    Validates price conditions based on the order type.
    
    - For LIMIT orders: price is required and must be greater than zero.
    - For MARKET orders: price should not be provided.
    
    Raises ValidationError if these conditions are violated.
    """
    if order_type == "LIMIT":
        if price is None:
            raise ValidationError("Price is required for LIMIT orders.")
        if price <= 0:
            raise ValidationError(f"Price must be greater than zero. Got {price}.")
    elif order_type == "MARKET" and price is not None:
        raise ValidationError("Price cannot be specified for MARKET orders.")


def validate_order_params(
    symbol: str, side: str, order_type: str, quantity: float, price: float | None
) -> None:
    """
    Validates all order parameters before calling the Binance API.
    
    Raises ValidationError if any parameter is invalid.
    """
    validate_symbol(symbol)
    validate_side(side)
    validate_type(order_type)
    validate_quantity(quantity)
    validate_price(price, order_type)
