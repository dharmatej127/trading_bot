"""
Flask server to expose the trading bot via a REST API for the frontend UI.
"""

import json
import logging
import os
from typing import Any

from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask import send_from_directory

from bot import (
    BinanceClient,
    BinanceAPIError,
    NetworkError,
    TradingBotError,
    ValidationError,
    place_limit_order,
    place_market_order,
    setup_logging,
    validate_order_params,
)

# Setup logging on startup
setup_logging()
logger = logging.getLogger("bot.server")

# Load environment credentials
load_dotenv()

app = Flask(__name__, static_folder="frontend", static_url_path="")


def get_binance_client() -> BinanceClient:
    """Initializes and returns a fresh BinanceClient from environment variables."""
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    base_url = os.getenv("BASE_URL", "https://testnet.binancefuture.com")

    if not api_key or not api_secret:
        raise ValidationError(
            "Missing API credentials. Please configure BINANCE_API_KEY and BINANCE_API_SECRET in your .env file."
        )

    return BinanceClient(api_key=api_key, api_secret=api_secret, base_url=base_url)


@app.route("/")
def index() -> Any:
    """Serve the frontend application."""
    return send_from_directory("frontend", "index.html")


@app.route("/api/place-order", methods=["POST"])
def place_order() -> Any:
    """
    Place a futures order via the REST API.

    Expects JSON body:
        {
            "symbol": "BTCUSDT",
            "side": "BUY",
            "type": "MARKET",
            "quantity": 0.001,
            "price": null  // optional, required for LIMIT
        }
    """
    data: dict = request.get_json(force=True)
    logger.info("Received order request via API: %s", data)

    symbol = str(data.get("symbol", "")).strip().upper()
    side = str(data.get("side", "")).strip().upper()
    order_type = str(data.get("type", "")).strip().upper()
    quantity_raw = data.get("quantity")
    price_raw = data.get("price")

    try:
        quantity = float(quantity_raw)
        price = float(price_raw) if price_raw is not None and price_raw != "" else None
    except (TypeError, ValueError):
        return jsonify({"success": False, "error": "Invalid quantity or price format."}), 400

    try:
        validate_order_params(symbol, side, order_type, quantity, price)
    except ValidationError as e:
        logger.warning("Validation error in API: %s", str(e))
        return jsonify({"success": False, "error": str(e)}), 422

    try:
        client = get_binance_client()

        if order_type == "MARKET":
            response = place_market_order(client=client, symbol=symbol, side=side, quantity=quantity)
        else:
            response = place_limit_order(
                client=client, symbol=symbol, side=side, quantity=quantity, price=price  # type: ignore
            )

        logger.info("Order placed successfully via API: %s", response)
        return jsonify({"success": True, "data": response}), 200

    except ValidationError as e:
        return jsonify({"success": False, "error": str(e)}), 422
    except BinanceAPIError as e:
        logger.error("Binance API error: %s", str(e), exc_info=True)
        return jsonify({"success": False, "error": f"Binance API Error: {e}"}), 502
    except NetworkError as e:
        logger.error("Network error: %s", str(e), exc_info=True)
        return jsonify({"success": False, "error": f"Network Error: {e}"}), 503
    except TradingBotError as e:
        logger.error("Trading bot error: %s", str(e), exc_info=True)
        return jsonify({"success": False, "error": str(e)}), 500
    except Exception as e:
        logger.error("Unexpected server error: %s", str(e), exc_info=True)
        return jsonify({"success": False, "error": "An unexpected server error occurred. Check logs."}), 500


if __name__ == "__main__":
    print("Starting Trading Bot Frontend Server on http://localhost:8080")
    app.run(debug=False, host="0.0.0.0", port=8080)
