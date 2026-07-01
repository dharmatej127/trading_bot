# Binance USDT-M Futures Trading Bot

A production-quality Python command-line interface (CLI) application for placing Market and Limit orders on the Binance USDT-M Futures Testnet.

## Project Overview

This trading bot provides a cleanly structured, reusable command-line interface built to senior backend engineering standards. It utilizes the official Binance Futures Testnet API, performs comprehensive local client-side validation before transmitting requests, manages API and network failures gracefully, and maintains detailed transaction logs without exposing API credentials.

---

## Features

- **Order Types Supported**: Market Orders and Limit Orders.
- **Order Sides**: `BUY` and `SELL`.
- **Target Market**: USDT-Margined (USDT-M) Futures Testnet.
- **Robust Local Validation**: Validates symbol conventions, side, order type constraints, positive quantity thresholds, and required price checks prior to sending requests to Binance.
- **Error Handling**: Custom exception hierarchies wrapping API/Network faults and displaying clean user-friendly CLI warnings rather than raw tracebacks.
- **Logging System**: Full logging configuration registering connection timeouts, failures, and transaction payloads to `logs/trading.log` (fully scrubbing secret keys).
- **Interactive UI**: CLI styling with visual colored cues using `colorama` and confirmation prompts to prevent unintended trades.

---

## Requirements

- **Python Version**: Python 3.11 or higher
- **Dependencies**:
  - `python-binance` (Official API client)
  - `python-dotenv` (Environment variable manager)
  - `colorama` (Terminal visual highlighting)
  - `requests` (Used internally for network layer actions)

---

## Installation

### 1. Clone or Move to the Workspace
Ensure your shell is positioned in the project root folder:
```bash
cd trading_bot
```

### 2. Set Up a Virtual Environment
Create and activate a python virtual environment:

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**On Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## Configuration

The bot retrieves credentials from a `.env` file located in the project root directory.

1. Duplicate the `.env.example` file:
   ```bash
   cp .env.example .env
   ```
   example : Open `.env` and fill in your Binance Futures Testnet API credentials:
   ```env
   BINANCE_API_KEY=your_testnet_api_key_here
   BINANCE_API_SECRET=your_testnet_api_secret_here
   BASE_URL=https://testnet.binancefuture.com
   ```
   2. Open `.env` and fill in your Binance Futures Testnet API credentials:
   ```env
   BINANCE_API_KEY=MQavemA6FfpQUAoJgwWdztVtDZupeJAG28Hatkyom056stqPSbQ81WvTLyeG8FHO
   BINANCE_API_SECRET=kArk5iCLRWjdmT9Ftyn0kAXeI70yaHpPm6S0dxIgppmiAfX9gWaiHXM8Q0Ipr0Fq
   BASE_URL=https://testnet.binancefuture.com
   ```

> [!WARNING]
> Never hardcode API keys or commit the `.env` file to version control.

---

## How to Run Examples & Manual Testing

Below are sample commands to test different components of the bot manually.

### 1. Place a Market Buy Order (USDT-M Futures Testnet)
Places a market buy order for 0.001 BTC:
```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```
*(Press `y` when prompted to confirm execution).*

### 2. Place a Limit Sell Order
Places a limit sell order for 0.002 BTC at $98,000:
```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.002 --price 98000
```
*(Press `y` when prompted to confirm execution).*

### 3. Verify Validator: Invalid Choice
Attempt to run with an invalid side (`HOLD`):
```bash
python cli.py --symbol BTCUSDT --side HOLD --type MARKET --quantity 0.001
```
*(Result: The CLI validation rejects the request automatically).*

### 4. Verify Validator: Missing Price on Limit Order
Attempt to place a LIMIT order without a price:
```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001
```
*(Result: `Error: Validation Error: Price is required for LIMIT orders.`)*


---

## Sample Output

When executing a valid command, the bot prints the order request, prompts for your confirmation, and outputs the response:

```text
========================
Order Request
========================
Symbol:   BTCUSDT
Side:     BUY
Type:     MARKET
Quantity: 0.001
========================

Do you want to proceed with placing this order? (y/n): y
Connecting to Binance Futures Testnet...
Executing order on Binance...

========================
Order Response
========================
Order ID:          284759201
Status:            FILLED
Executed Quantity: 0.001
Average Price:     96250.50
Client Order ID:   gX2kL8mPq1zR5sT7uV9wY
Timestamp:         1780309202000
========================

Order placed successfully.
```

---

## Project Structure

```text
trading_bot/
├── bot/
│   ├── __init__.py          # Package initialization & public imports
│   ├── client.py            # Reusable wrapper client for Binance
│   ├── orders.py            # Order layer functions (place_market_order, etc.)
│   ├── validators.py        # Validation rules for order payloads
│   ├── exceptions.py        # Package exception hierarchy
│   ├── logging_config.py    # Log configurations for console/file outputs
│   └── utils.py             # UI utilities, console colors, print handlers
├── logs/
│   └── trading.log          # Detailed application runtime log file
├── .env.example             # Example configuration template
├── .gitignore               # Ignored local files list
├── cli.py                   # Primary application CLI script
├── README.md                # Project documentation
└── requirements.txt         # Package dependencies
```

---

## Logging

All transaction steps are automatically written to `logs/trading.log`. Each entry contains:
- Timestamp
- API Endpoint called
- Request Payload (excluding API keys and secrets)
- Response Payload (or error details/stack traces if failed)

Example entry in `trading.log`:
```text
2026-07-01 10:20:01,102 - bot.cli - INFO - CLI invoked with args - Symbol: BTCUSDT, Side: BUY, Type: MARKET, Quantity: 0.001, Price: None
2026-07-01 10:20:01,895 - bot.client - INFO - Sending Futures Order Request to /fapi/v1/order. Payload: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001}
```

---

## Assumptions

- **USDT-M Futures**: The bot interacts exclusively with USDT-Margined Futures. Other instruments (e.g., COIN-M, Spot) are not supported.
- **Time In Force**: Limit orders default to `GTC` (Good Till Cancelled).
- **Default Testnet Base URL**: If `BASE_URL` is not specified, it falls back to `https://testnet.binancefuture.com`.

---

## Troubleshooting

- **Validation Error: Price is required for LIMIT orders**:
  You selected order type `LIMIT` but failed to provide the `--price` flag. Please append `--price <value>` to your command.
- **Missing API credentials**:
  Ensure you have created a `.env` file in the same directory as `cli.py` with your correct API key and secret.
- **Network connection failed**:
  Verify your internet connection and verify that `testnet.binancefuture.com` is accessible from your network.
