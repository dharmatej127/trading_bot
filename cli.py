#!/usr/bin/env python3
"""
Command Line Interface (CLI) for the Binance Futures Trading Bot.
"""

import os
import sys
import argparse
import logging
from dotenv import load_dotenv

from bot import (
    BinanceClient,
    place_market_order,
    place_limit_order,
    ValidationError,
    BinanceAPIError,
    NetworkError,
    TradingBotError,
    validate_order_params,
    setup_logging,
    print_success,
    print_error,
    print_info,
    print_warning,
    ask_confirmation,
    print_order_request,
    print_order_response,
)

# Initialize logger for the CLI module
logger = logging.getLogger("bot.cli")


def parse_arguments() -> argparse.Namespace:
    """
    Parses command line arguments for the trading bot.
    """
    parser = argparse.ArgumentParser(
        description="Place orders on the Binance USDT-M Futures Testnet."
    )
    parser.add_argument(
        "--symbol",
        type=str,
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT, ETHUSDT)",
    )
    parser.add_argument(
        "--side",
        type=str,
        required=True,
        choices=["BUY", "SELL"],
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type",
        type=str,
        required=True,
        choices=["MARKET", "LIMIT"],
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity",
        type=float,
        required=True,
        help="Order quantity (greater than 0)",
    )
    parser.add_argument(
        "--price",
        type=float,
        default=None,
        help="Order price (required only for LIMIT orders)",
    )
    return parser.parse_args()


def main() -> None:
    """
    Main entry point for the CLI trading bot application.
    """
    # 1. Setup logging configuration first
    setup_logging()

    # 2. Parse arguments
    args = parse_arguments()

    # Convert symbol, side, type to uppercase for standardisation
    symbol = args.symbol.strip().upper()
    side = args.side.strip().upper()
    order_type = args.type.strip().upper()
    quantity = args.quantity
    price = args.price

    logger.info(
        "CLI invoked with args - Symbol: %s, Side: %s, Type: %s, Quantity: %s, Price: %s",
        symbol,
        side,
        order_type,
        quantity,
        price,
    )

    # 3. Validate Inputs locally before hitting Binance API
    try:
        validate_order_params(symbol, side, order_type, quantity, price)
    except ValidationError as e:
        logger.warning("Local validation failed: %s", str(e))
        print_error(f"Validation Error: {e}")
        sys.exit(1)

    # 4. Load env credentials and check existence
    load_dotenv()
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = os.getenv("BASE_URL", "https://testnet.binancefuture.com")

    if not api_key or not api_secret:
        msg = "Missing API credentials. Please configure BINANCE_API_KEY and BINANCE_API_SECRET in your .env file."
        logger.error(msg)
        print_error(msg)
        sys.exit(1)

    # 5. Display Order Request and get User Confirmation (Bonus Feature)
    print_order_request(symbol, side, order_type, quantity, price)
    
    if not ask_confirmation("Do you want to proceed with placing this order?"):
        logger.info("Order placement cancelled by user.")
        print_warning("Order execution cancelled.")
        sys.exit(0)

    # 6. Initialize Client and execute Order
    try:
        print_info("Connecting to Binance Futures Testnet...")
        client = BinanceClient(api_key=api_key, api_secret=api_secret, base_url=base_url)

        print_info("Executing order on Binance...")
        if order_type == "MARKET":
            response = place_market_order(
                client=client, symbol=symbol, side=side, quantity=quantity
            )
        else:
            # Type is validated as LIMIT, price is guaranteed not to be None
            response = place_limit_order(
                client=client, symbol=symbol, side=side, quantity=quantity, price=price  # type: ignore
            )

        # 7. Print order response details
        print_order_response(response)

    except ValidationError as e:
        # Catch validation error if any occurs at client level
        logger.error("Validation failure: %s", str(e), exc_info=True)
        print_error(str(e))
        sys.exit(1)
    except BinanceAPIError as e:
        # Handled API error
        logger.error("Binance API error: %s", str(e), exc_info=True)
        print_error(f"Binance API returned an error: {e}")
        sys.exit(1)
    except NetworkError as e:
        # Handled network failure/timeout
        logger.error("Network or connection error: %s", str(e), exc_info=True)
        print_error(f"Network error: {e}")
        sys.exit(1)
    except TradingBotError as e:
        # Other package exceptions
        logger.error("Trading bot error: %s", str(e), exc_info=True)
        print_error(f"Trading bot encountered an error: {e}")
        sys.exit(1)
    except Exception as e:
        # Catch-all for unexpected exceptions
        logger.error("An unexpected error occurred: %s", str(e), exc_info=True)
        print_error("An unexpected system error occurred. Please check the logs.")
        sys.exit(1)


if __name__ == "__main__":
    main()
