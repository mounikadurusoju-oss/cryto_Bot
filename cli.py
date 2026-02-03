#!/usr/bin/env python3
"""CLI entry point for the Binance Futures Trading Bot."""
import argparse
import sys

from bot.client import get_client, ClientError
from bot.orders import place_order, OrderError
from bot.validators import validate_order_params, ValidationError


def parse_args() -> argparse.Namespace:
    """Parse command-line arguments.

    Returns:
        Parsed arguments namespace.
    """
    parser = argparse.ArgumentParser(
        description="Binance Futures Testnet Trading Bot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  Market order:  python cli.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001
  Limit order:   python cli.py --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.001 --price 50000
        """,
    )

    parser.add_argument(
        "--symbol",
        required=True,
        help="Trading pair symbol (e.g., BTCUSDT)",
    )
    parser.add_argument(
        "--side",
        required=True,
        choices=["BUY", "SELL", "buy", "sell"],
        help="Order side: BUY or SELL",
    )
    parser.add_argument(
        "--type",
        required=True,
        dest="order_type",
        choices=["MARKET", "LIMIT", "market", "limit"],
        help="Order type: MARKET or LIMIT",
    )
    parser.add_argument(
        "--quantity",
        required=True,
        help="Order quantity",
    )
    parser.add_argument(
        "--price",
        required=False,
        help="Order price (required for LIMIT orders)",
    )

    return parser.parse_args()


def print_request_summary(params: dict) -> None:
    """Print a summary of the order request.

    Args:
        params: Validated order parameters.
    """
    print("\n=== ORDER REQUEST ===")
    print(f"Symbol:   {params['symbol']}")
    print(f"Side:     {params['side']}")
    print(f"Type:     {params['order_type']}")
    print(f"Quantity: {params['quantity']}")
    if params['price'] is not None:
        print(f"Price:    {params['price']}")
    print()


def print_response(response: dict) -> None:
    """Print the order response details.

    Args:
        response: Order response from the API.
    """
    print("=== ORDER RESPONSE ===")
    print(f"Order ID:     {response['orderId']}")
    print(f"Status:       {response['status']}")
    print(f"Executed Qty: {response['executedQty']}")
    print(f"Avg Price:    {response['avgPrice']}")
    print("\n=== ORDER PLACED SUCCESSFULLY ===\n")


def print_error(message: str) -> None:
    """Print an error message.

    Args:
        message: The error message to display.
    """
    print(f"\n=== ORDER FAILED ===")
    print(f"Error: {message}")
    print()


def main() -> int:
    """Main entry point for the trading bot CLI.

    Returns:
        Exit code (0 for success, 1 for failure).
    """
    args = parse_args()

    # Step 1: Validate inputs
    try:
        params = validate_order_params(
            symbol=args.symbol,
            side=args.side,
            order_type=args.order_type,
            quantity=args.quantity,
            price=args.price,
        )
    except ValidationError as e:
        print_error(str(e))
        return 1

    # Step 2: Print request summary
    print_request_summary(params)

    # Step 3: Initialize client
    try:
        client = get_client()
    except ClientError as e:
        print_error(str(e))
        return 1

    # Step 4: Place order
    try:
        response = place_order(
            client=client,
            symbol=params["symbol"],
            side=params["side"],
            order_type=params["order_type"],
            quantity=params["quantity"],
            price=params["price"],
        )
    except OrderError as e:
        print_error(str(e))
        return 1

    # Step 5: Print response
    print_response(response)

    return 0


if __name__ == "__main__":
    sys.exit(main())
