"""
Binance API client wrapper.
"""

import logging
from typing import Any
from binance.client import Client
from binance.exceptions import BinanceAPIException
from requests.exceptions import RequestException, Timeout

from bot.exceptions import BinanceAPIError, NetworkError

logger = logging.getLogger(__name__)


class BinanceClient:
    """
    Wrapper around the python-binance Client for futures trading on the testnet.
    """

    def __init__(self, api_key: str, api_secret: str, base_url: str):
        """
        Initializes the BinanceClient wrapper.
        
        API credentials and base url are injected.
        """
        self.api_key = api_key
        self.api_secret = api_secret
        self.base_url = base_url

        # Scrub keys in logs
        logger.info("Initializing BinanceClient with provided API Key and Secret (credentials scrubbed)")

        try:
            # Check if base_url indicates testnet (default futures testnet is testnet.binancefuture.com)
            is_testnet = "testnet" in base_url.lower()
            
            # Initialize python-binance Client
            self.client = Client(
                api_key=self.api_key,
                api_secret=self.api_secret,
                testnet=is_testnet
            )
            
            # If a custom base URL is provided, we can override the FUTURES_URL endpoint if needed.
            # In python-binance, client.FUTURES_URL is used for futures calls.
            if is_testnet:
                # python-binance sets FUTURES_URL to 'https://testnet.binancefuture.com/fapi'
                pass
            else:
                # If custom base url, map it properly
                if not base_url.endswith("/fapi"):
                    self.client.FUTURES_URL = f"{base_url.rstrip('/')}/fapi"
                else:
                    self.client.FUTURES_URL = base_url
                    
            logger.info("Binance Futures Client successfully initialized. Base URL: %s", self.client.FUTURES_URL)
            
        except Exception as e:
            logger.error("Failed to initialize Binance Client: %s", str(e), exc_info=True)
            raise NetworkError(f"Failed to initialize Binance Client: {e}") from e

    def execute_futures_order(
        self, symbol: str, side: str, order_type: str, quantity: float, price: float | None = None
    ) -> dict[str, Any]:
        """
        Executes a futures order on USDT-M Futures.
        
        Handles exceptions, logs requests and responses (without secrets),
        and returns a structured dict of the result.
        """
        # Prepare endpoint and request payload
        endpoint = "/fapi/v1/order"
        payload = {
            "symbol": symbol,
            "side": side,
            "type": order_type,
            "quantity": quantity,
        }
        if price is not None:
            payload["price"] = price
            # Limit orders require timeInForce. Default to GTC (Good Till Cancelled)
            payload["timeInForce"] = "GTC"

        logger.info("Sending Futures Order Request to %s. Payload: %s", endpoint, payload)

        try:
            # Call python-binance client futures_create_order
            # This makes a POST request to FUTURES_URL + /v1/order
            response = self.client.futures_create_order(**payload)
            
            logger.info("Received Futures Order Response from %s. Response: %s", endpoint, response)
            
            # Map response to expected structure
            # Example response fields: orderId, status, executedQty, avgPrice, clientOrderId, updateTime
            # In case avgPrice is empty or 0, we can fall back to price or other logic.
            return {
                "order_id": response.get("orderId"),
                "status": response.get("status"),
                "executed_qty": response.get("executedQty"),
                "avg_price": response.get("avgPrice") or response.get("price"),
                "client_order_id": response.get("clientOrderId"),
                "update_time": response.get("updateTime"),
            }

        except BinanceAPIException as e:
            error_msg = f"Binance API Error: [Code: {e.code}] {e.message}"
            logger.error("%s. Request Payload: %s", error_msg, payload)
            raise BinanceAPIError(message=e.message, code=e.code, response=e.response) from e

        except Timeout as e:
            error_msg = "Binance API request timed out."
            logger.error("%s. Request Payload: %s", error_msg, payload, exc_info=True)
            raise NetworkError(error_msg) from e

        except RequestException as e:
            error_msg = f"Network connection failed: {e}"
            logger.error("%s. Request Payload: %s", error_msg, payload, exc_info=True)
            raise NetworkError(error_msg) from e

        except Exception as e:
            error_msg = f"Unexpected error during order placement: {e}"
            logger.error("%s. Request Payload: %s", error_msg, payload, exc_info=True)
            raise NetworkError(error_msg) from e
