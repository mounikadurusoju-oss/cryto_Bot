"""Binance Futures Testnet client wrapper."""
import os
from typing import Optional

from binance.client import Client
from binance.exceptions import BinanceAPIException
from dotenv import load_dotenv

from .logging_config import get_logger

logger = get_logger(__name__)


class ClientError(Exception):
    """Raised when client initialization or connection fails."""
    pass


def get_client() -> Client:
    """Create and return an authenticated Binance Futures Testnet client.

    Loads API credentials from environment variables and initializes
    the client with testnet=True.

    Returns:
        An authenticated Binance Client instance.

    Raises:
        ClientError: If credentials are missing or authentication fails.
    """
    load_dotenv()

    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")

    if not api_key or not api_secret:
        raise ClientError(
            "Missing API credentials. Please set BINANCE_API_KEY and "
            "BINANCE_API_SECRET in your .env file."
        )

    try:
        client = Client(api_key, api_secret, testnet=True)
        logger.info("Binance Testnet client initialized successfully.")
        return client
    except BinanceAPIException as e:
        logger.error(f"Failed to initialize Binance client: {e}")
        raise ClientError(f"Authentication failed: {e.message}")
    except Exception as e:
        logger.error(f"Unexpected error initializing client: {e}")
        raise ClientError(f"Failed to connect to Binance: {e}")
