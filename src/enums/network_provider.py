"""Network provider enum."""

from enum import Enum


class NetworkProvider(str, Enum):
    """Network provider enum."""

    MTN = "MTN"
    AIRTEL = "ATL"
    VODAFONE = "VOD"
