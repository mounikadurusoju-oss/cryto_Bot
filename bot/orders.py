"""Order placement logic for Binance Testnet."""
from typing import Any, Dict, Optional

from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
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
    """Place an order on Binance Testnet.

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
        params["timeInForce"] = TIME_IN_FORCE_GTC

    logger.info(f"Placing order: {params}")

    try:
        response = client.create_order(**params)
        logger.info(f"Order response: {response}")

        # Calculate average price from fills if available
        avg_price = "N/A"
        if response.get("fills"):
            total_qty = sum(float(f["qty"]) for f in response["fills"])
            total_value = sum(float(f["qty"]) * float(f["price"]) for f in response["fills"])
            if total_qty > 0:
                avg_price = str(round(total_value / total_qty, 2))
        elif response.get("price"):
            avg_price = response["price"]

        result = {
            "orderId": response.get("orderId"),
            "status": response.get("status"),
            "executedQty": response.get("executedQty"),
            "avgPrice": avg_price,
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
