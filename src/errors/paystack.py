"""Paystack errors."""


class PaystackError(Exception):
    """Base class for Paystack errors."""

    def __init__(self, message: str, status_code: int = 400) -> None:
        self.message = message
        self.status_code = status_code


class PaystackSystemMalfunctionError(PaystackError):
    """A system malfunction error."""

    def __init__(
        self, message: str = "System Malfunction. Please retry the transfer."
    ) -> None:
        super().__init__(message, status_code=500)


class PaystackMaxTransactionLimitError(PaystackError):
    """Max Transaction Limit."""

    def __init__(
        self,
        message: str = "You have exceeded the maximum transaction limit of 50,000 GHS.",
    ) -> None:
        super().__init__(message, status_code=400)


class PaystackMinTransactionLimitError(PaystackError):
    """Min Transaction Limit."""

    def __init__(
        self, message: str = "The minimum amount you may send is 1.00 GHS."
    ) -> None:
        super().__init__(message, status_code=400)


class PaystackAccountNumberError(PaystackError):
    """An account number error."""

    def __init__(self, message: str = "Account number is required.") -> None:
        super().__init__(message, status_code=400)


class PaystackInvalidTransferRecipientError(PaystackError):
    """Invalid transfer recipient code."""

    def __init__(self, message: str = "Invalid wallet ID.") -> None:
        super().__init__(message, status_code=400)


class PaystackInvalidProviderError(PaystackError):
    """Invalid provider error."""

    def __init__(self, message: str = "Invalid provider.") -> None:
        super().__init__(message, status_code=400)


class PaystackIncorrectOTPError(PaystackError):
    """Incorrect OTP error."""

    def __init__(self, message: str = "Incorrect OTP.") -> None:
        super().__init__(message, status_code=400)