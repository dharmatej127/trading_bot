"""
Custom exception classes for the trading bot application.
"""

class TradingBotError(Exception):
    """Base exception class for all errors in the trading bot."""
    pass


class ValidationError(TradingBotError):
    """Raised when validation of arguments or order parameters fails."""
    pass


class BinanceAPIError(TradingBotError):
    """Raised when the Binance API returns an error response."""
    
    def __init__(self, message: str, code: int | None = None, response: dict | None = None):
        super().__init__(message)
        self.code = code
        self.response = response


class NetworkError(TradingBotError):
    """Raised when a network connectivity issue or timeout occurs."""
    pass
