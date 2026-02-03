"""Order placement logic for Binance Futures."""
from typing import Any, Dict, Optional

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
import requests

from .logging_config import get_logger

logger = get_logger(__name__)


class OrderError(Exception):
    """Raised when order placement fails."""
    pass


def place_order(
    client: Client,
    symbol: str,
    side: str,
    order_type: str,
    quantity: float,
    price: Optional[float] = None,
) -> Dict[str, Any]:
    """Place an order on Binance Futures Testnet.

    Args:
        client: An authenticated Binance Client instance.
        symbol: The trading pair symbol (e.g., BTCUSDT).
        side: The order side (BUY or SELL).
        order_type: The order type (MARKET or LIMIT).
        quantity: The order quantity.
        price: The order price (required for LIMIT orders).

    Returns:
        A dictionary containing order response details:
        - orderId: The unique order identifier
        - status: The order status (e.g., FILLED, NEW)
        - executedQty: The executed quantity
        - avgPrice: The average fill price (if available)

    Raises:
        OrderError: If the order placement fails.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity,
    }

    if order_type == "LIMIT":
        params["price"] = price
        params["timeInForce"] = "GTC"

    logger.info(f"Placing order: {params}")

    try:
        response = client.futures_create_order(**params)
        logger.info(f"Order response: {response}")

        result = {
            "orderId": response.get("orderId"),
            "status": response.get("status"),
            "executedQty": response.get("executedQty"),
            "avgPrice": response.get("avgPrice", "N/A"),
        }

        return result

    except BinanceOrderException as e:
        logger.error(f"Order error: {e.message}")
        raise OrderError(f"Order rejected: {e.message}")

    except BinanceAPIException as e:
        logger.error(f"API error: {e.message}")
        raise OrderError(f"API error: {e.message}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error: {e}")
        raise OrderError(f"Network error: Unable to connect to Binance. Please check your internet connection.")

    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise OrderError(f"Unexpected error: {e}")
