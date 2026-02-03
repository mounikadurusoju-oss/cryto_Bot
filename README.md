# Binance Futures Trading Bot

A command-line trading bot for placing orders on Binance Futures Testnet (USDT-M). This bot provides a clean, reusable structure with proper logging and comprehensive error handling.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
  - [Command Syntax](#command-syntax)
  - [Arguments](#arguments)
  - [Examples](#examples)
- [Project Structure](#project-structure)
- [Architecture](#architecture)
- [Logging](#logging)
- [Error Handling](#error-handling)
- [Assumptions](#assumptions)
- [Troubleshooting](#troubleshooting)

## Features

- Place **Market** and **Limit** orders on Binance Futures Testnet
- Support for both **BUY** and **SELL** order sides
- Comprehensive input validation before API calls
- Structured logging to file for debugging and audit trails
- Clean separation of concerns (CLI layer / API layer)
- Robust exception handling for various failure scenarios
- Case-insensitive input handling (accepts both "BUY" and "buy")

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- Binance Futures Testnet account with API credentials
- Internet connection

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/mounikadurusoju-oss/cryto_Bot.git
cd cryto_Bot
```

### 2. Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Get Binance Futures Testnet API Credentials

1. Visit [Binance Futures Testnet](https://testnet.binancefuture.com)
2. Register for a testnet account (separate from your real Binance account)
3. Navigate to API Management section
4. Generate a new API key pair
5. Copy both the **API Key** and **Secret Key**

### 2. Set Up Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your credentials
nano .env  # or use any text editor
```

Add your credentials to the `.env` file:

```env
BINANCE_API_KEY=your_actual_api_key_here
BINANCE_API_SECRET=your_actual_secret_key_here
```

**Important:** Never commit your `.env` file to version control. It's already included in `.gitignore`.

## Usage

### Command Syntax

```bash
python cli.py --symbol <SYMBOL> --side <BUY|SELL> --type <MARKET|LIMIT> --quantity <QTY> [--price <PRICE>]
```

### Arguments

| Argument     | Required | Description                              |
|--------------|----------|------------------------------------------|
| `--symbol`   | Yes      | Trading pair symbol (e.g., BTCUSDT)      |
| `--side`     | Yes      | Order side: `BUY` or `SELL`              |
| `--type`     | Yes      | Order type: `MARKET` or `LIMIT`          |
| `--quantity` | Yes      | Order quantity (e.g., 0.001)             |
| `--price`    | No*      | Order price (*required for LIMIT orders) |

### Examples

#### Market Order - Buy BTC

```bash
python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
```

#### Market Order - Sell ETH

```bash
python cli.py --symbol ETHUSDT --side SELL --type MARKET --quantity 0.01
```

#### Limit Order - Buy BTC at specific price

```bash
python cli.py --symbol BTCUSDT --side BUY --type LIMIT --quantity 0.001 --price 40000
```

#### Limit Order - Sell BTC at specific price

```bash
python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 50000
```

### Sample Output

**Successful Order:**

```
=== ORDER REQUEST ===
Symbol:   BTCUSDT
Side:     BUY
Type:     MARKET
Quantity: 0.001

=== ORDER RESPONSE ===
Order ID:     12345678
Status:       FILLED
Executed Qty: 0.001
Avg Price:    43250.50

=== ORDER PLACED SUCCESSFULLY ===
```

**Failed Order:**

```
=== ORDER FAILED ===
Error: Price is required for LIMIT orders.
```

## Project Structure

```
trading_bot/
├── bot/
│   ├── __init__.py           # Package initialization
│   ├── client.py             # Binance API client wrapper
│   ├── orders.py             # Order placement logic
│   ├── validators.py         # Input validation functions
│   └── logging_config.py     # Logging configuration
├── cli.py                    # CLI entry point (main script)
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
└── trading.log               # Log file (generated at runtime)
```

## Architecture

The application follows a layered architecture for clean separation of concerns:

```
┌─────────────────────────────────────────────────────────┐
│                      CLI Layer                          │
│                      (cli.py)                           │
│         - Parses command-line arguments                 │
│         - Displays output to user                       │
│         - Orchestrates the order flow                   │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                  Validation Layer                       │
│                  (validators.py)                        │
│         - Validates all user inputs                     │
│         - Normalizes data (uppercase, type conversion)  │
│         - Raises ValidationError on invalid input       │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Order Layer                           │
│                   (orders.py)                           │
│         - Constructs order parameters                   │
│         - Calls Binance API                             │
│         - Handles API responses and errors              │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│                   Client Layer                          │
│                   (client.py)                           │
│         - Manages API authentication                    │
│         - Initializes Binance client                    │
│         - Handles connection errors                     │
└─────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────┐
│              Binance Futures Testnet API                │
│           https://testnet.binancefuture.com             │
└─────────────────────────────────────────────────────────┘
```

## Logging

All API requests, responses, and errors are logged to `trading.log` in the project root directory.

### Log Format

```
TIMESTAMP - MODULE - LEVEL - MESSAGE
```

### Example Log Entries

```
2024-01-15 10:30:45 - bot.client - INFO - Binance Testnet client initialized successfully.
2024-01-15 10:30:45 - bot.orders - INFO - Placing order: {'symbol': 'BTCUSDT', 'side': 'BUY', 'type': 'MARKET', 'quantity': 0.001}
2024-01-15 10:30:46 - bot.orders - INFO - Order response: {'orderId': 12345678, 'status': 'FILLED', 'executedQty': '0.001', 'avgPrice': '43250.50'}
```

### Log Levels

- **INFO**: Successful operations (client initialization, order placement, responses)
- **ERROR**: Failed operations (API errors, network failures, validation errors)

## Error Handling

The bot handles multiple error scenarios gracefully:

| Error Type | Description | Example |
|------------|-------------|---------|
| **ValidationError** | Invalid user input | Missing price for LIMIT order |
| **ClientError** | API credential issues | Missing or invalid API keys |
| **OrderError** | Order placement failures | Insufficient funds, invalid symbol |
| **Network Error** | Connection problems | Timeout, no internet connection |

### Error Examples

**Missing API Credentials:**
```
=== ORDER FAILED ===
Error: Missing API credentials. Please set BINANCE_API_KEY and BINANCE_API_SECRET in your .env file.
```

**Invalid Symbol:**
```
=== ORDER FAILED ===
Error: Invalid symbol 'INVALID'. Only USDT-M pairs are supported (e.g., BTCUSDT).
```

**Missing Price for LIMIT Order:**
```
=== ORDER FAILED ===
Error: Price is required for LIMIT orders.
```

## Assumptions

1. **USDT-M Pairs Only**: The bot only supports USDT-margined futures pairs (symbols ending with USDT)
2. **Testnet Environment**: The bot is configured exclusively for Binance Futures Testnet
3. **Time-in-Force**: LIMIT orders use GTC (Good Till Cancelled) as the default time-in-force
4. **System Clock**: The host machine's clock should be synchronized for timestamp validation
5. **Single Order Mode**: The bot places one order per execution (no batch orders)

## Troubleshooting

### Common Issues

**1. "Missing API credentials" error**
- Ensure `.env` file exists in the project root
- Verify API key and secret are correctly set
- Check there are no extra spaces in the `.env` file

**2. "Timestamp for this request is outside of the recvWindow"**
- Synchronize your system clock with an NTP server
- On Linux: `sudo ntpdate time.nist.gov`

**3. "Invalid symbol" error**
- Ensure the symbol exists on Binance Futures
- Symbol must end with USDT (e.g., BTCUSDT, ETHUSDT)

**4. "Connection error"**
- Check your internet connection
- Verify firewall is not blocking outbound connections
- Try again after a few seconds

**5. Import errors**
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt` again

## Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| python-binance | >=1.0.19 | Binance API wrapper |
| python-dotenv | >=1.0.0 | Environment variable management |

## License

MIT License
