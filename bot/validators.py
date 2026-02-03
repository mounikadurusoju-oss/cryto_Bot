"""Input validation for trading bot parameters."""
from typing import Optional


class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


def validate_symbol(symbol: str) -> str:
    """Validate the trading symbol.

    Args:
        symbol: The trading pair symbol (e.g., BTCUSDT).

    Returns:
        The validated symbol in uppercase.

    Raises:
        ValidationError: If the symbol is invalid.
    """
    if not symbol:
        raise ValidationError("Symbol is required.")

    symbol = symbol.upper()

    if not symbol.endswith("USDT"):
        raise ValidationError(
            f"Invalid symbol '{symbol}'. Only USDT-M pairs are supported (e.g., BTCUSDT)."
        )

    return symbol


def validate_side(side: str) -> str:
    """Validate the order side.

    Args:
        side: The order side (BUY or SELL).

    Returns:
        The validated side in uppercase.

    Raises:
        ValidationError: If the side is invalid.
    """
    if not side:
        raise ValidationError("Side is required.")

    side = side.upper()
    valid_sides = ("BUY", "SELL")

    if side not in valid_sides:
        raise ValidationError(
            f"Invalid side '{side}'. Must be one of: {', '.join(valid_sides)}."
        )

    return side


def validate_order_type(order_type: str) -> str:
    """Validate the order type.

    Args:
        order_type: The order type (MARKET or LIMIT).

    Returns:
        The validated order type in uppercase.

    Raises:
        ValidationError: If the order type is invalid.
    """
    if not order_type:
        raise ValidationError("Order type is required.")

    order_type = order_type.upper()
    valid_types = ("MARKET", "LIMIT")

    if order_type not in valid_types:
        raise ValidationError(
            f"Invalid order type '{order_type}'. Must be one of: {', '.join(valid_types)}."
        )

    return order_type


def validate_quantity(quantity: str) -> float:
    """Validate the order quantity.

    Args:
        quantity: The order quantity as a string.

    Returns:
        The validated quantity as a float.

    Raises:
        ValidationError: If the quantity is invalid.
    """
    if not quantity:
        raise ValidationError("Quantity is required.")

    try:
        qty = float(quantity)
    except ValueError:
        raise ValidationError(f"Invalid quantity '{quantity}'. Must be a number.")

    if qty <= 0:
        raise ValidationError(
            f"Invalid quantity '{qty}'. Must be greater than zero."
        )

    return qty


def validate_price(price: Optional[str], order_type: str) -> Optional[float]:
    """Validate the order price.

    Args:
        price: The order price as a string (optional for MARKET orders).
        order_type: The order type (MARKET or LIMIT).

    Returns:
        The validated price as a float, or None for MARKET orders.

    Raises:
        ValidationError: If the price is invalid or missing for LIMIT orders.
    """
    if order_type == "LIMIT":
        if not price:
            raise ValidationError("Price is required for LIMIT orders.")

        try:
            p = float(price)
        except ValueError:
            raise ValidationError(f"Invalid price '{price}'. Must be a number.")

        if p <= 0:
            raise ValidationError(
                f"Invalid price '{p}'. Must be greater than zero."
            )

        return p

    return None


def validate_order_params(
    symbol: str,
    side: str,
    order_type: str,
    quantity: str,
    price: Optional[str] = None,
) -> dict:
    """Validate all order parameters.

    Args:
        symbol: The trading pair symbol.
        side: The order side (BUY or SELL).
        order_type: The order type (MARKET or LIMIT).
        quantity: The order quantity.
        price: The order price (required for LIMIT orders).

    Returns:
        A dictionary with validated parameters.

    Raises:
        ValidationError: If any parameter is invalid.
    """
    validated_type = validate_order_type(order_type)

    return {
        "symbol": validate_symbol(symbol),
        "side": validate_side(side),
        "order_type": validated_type,
        "quantity": validate_quantity(quantity),
        "price": validate_price(price, validated_type),
    }
