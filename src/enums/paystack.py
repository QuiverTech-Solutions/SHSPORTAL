"""Paystack enums."""

from enum import Enum


class RecipientTransferCreateType(str, Enum):
    """Enum for recipient transfer create type."""

    BANK = "ghipss"
    MOBILE_MONEY = "mobile_money"


class AvailableBankCountries(str, Enum):
    """Enum for available bank countries."""

    GHANA = "ghana"
    KENYA = "kenya"
    NIGERIA = "nigeria"
    SOUTH_AFRICA = "south_africa"
