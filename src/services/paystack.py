"""Paystack service module."""

import hashlib
import hmac
from typing import Any

import httpx
from fastapi import HTTPException

from models.paystack.payment import CreateVotingUSSDPayment
from src.core.config import PAYSTACK_BASE_URL, PAYSTACK_SECRET_KEY
from src.errors.paystack import (
    PaystackAccountNumberError,
    PaystackError,
    PaystackIncorrectOTPError,
    PaystackInvalidProviderError,
    PaystackInvalidTransferRecipientError,
    PaystackMaxTransactionLimitError,
    PaystackMinTransactionLimitError,
    PaystackSystemMalfunctionError,
)
from src.models.paystack.charge import ChargeOTPVerifyRequest, ChargeResponse
from src.models.paystack.transfer import TransferRequest, TransferResponse
from src.utils.helpers import Helpers


class PaystackService:
    """A class to handle Paystack API requests."""

    def __init__(self) -> None:
        """Initialize the Paystack class."""
        self.base_url = PAYSTACK_BASE_URL
        self.secret_key = PAYSTACK_SECRET_KEY

    async def create_ussd_payment(
        self,
        create_payment: CreateVotingUSSDPayment,
    ) -> ChargeResponse:
        """This function creates a mobile money payment transaction using the Paystack API with the specified email and amount."""
        if create_payment.amount < 1:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        url = f"{self.base_url}charge"
        reference = Helpers.generate_transaction_id(
            create_payment.phone_number, create_payment.student_name
        )
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }

        data = {
            "amount": float(create_payment.amount) * 100,
            "email": "QuiverTech1@gmail.com",
            "currency": "GHS",
            "mobile_money": {
                "phone": create_payment.phone_number,
                "provider": create_payment.network_provider.value,
            },
            "metadata": {
                "custom_fields": [
                    {
                        "display_name": "School name",
                        "variable_name": "School name",
                        "value": create_payment.school_name,
                    },
                    {
                        "display_name": "Student name",
                        "variable_name": "Student name",
                        "value": create_payment.student_name,
                    },
                    {
                        "display_name": "School ID",
                        "variable_name": "School ID",
                        "value": str(create_payment.school_id),
                    },
                    {
                        "display_name": "Total amount",
                        "variable_name": "Amount paid",
                        "value": float(create_payment.amount),
                    },
                    {
                        "display_name": "School amount",
                        "variable_name": "School amount",
                        "value": float(create_payment.amount) * 0.8,
                    },
                    {
                        "display_name": "Admin amount",
                        "variable_name": "Admin amount",
                        "value": float(create_payment.amount) * 0.2,
                    },
                    {
                        "display_name": "Network provider",
                        "variable_name": "Network provider",
                        "value": create_payment.network_provider.value,
                    },
                    {
                        "display_name": "Phone Number",
                        "variable_name": "Phone Number",
                        "value": create_payment.phone_number,
                    },
                ]
            },
            "reference": reference,
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response_data: dict[str, Any] = response.json()
            print(response_data)

            if response.status_code != 200 or not response_data.get("status"):
                error_message = response_data.get("message", "Unknown error occurred")
                if "invalid provider" in error_message.lower():
                    raise PaystackInvalidProviderError()
                elif "maximum amount" in error_message.lower():
                    raise PaystackMaxTransactionLimitError()
                elif "minimum amount you may send" in error_message.lower():
                    raise PaystackMinTransactionLimitError()
                else:
                    raise PaystackError("Unexpected error", response.status_code)

            response.raise_for_status()

            return ChargeResponse(**response_data)

    async def verify_ussd_otp_payment(
        self, otp_data: ChargeOTPVerifyRequest
    ) -> httpx.Response:
        """This function verifies a USSD payment transaction using the Paystack API."""
        url = f"{self.base_url}charge/submit_otp"
        headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json",
        }
        data = {
            "reference": otp_data.reference,
            "otp": otp_data.otp,
        }

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=data)
            response_data: dict[str, Any] = response.json()
            print(response_data)

            if response.status_code != 200 or not response_data.get("status"):
                error_message = response_data.get("message", "Unknown error occurred")
                if "The otp provided is incorrect" in error_message.lower():
                    raise PaystackIncorrectOTPError()
                else:
                    raise PaystackError("Unexpected error", response.status_code)

            response.raise_for_status()
            return ChargeResponse(**response_data)

    async def verify_transaction(self, reference: str) -> httpx.Response:
        """This function verifies a paystack transaction. It returns the status of the transaction."""
        try:
            url = f"{self.base_url}transaction/verify/{reference}"
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json",
            }
            async with httpx.AsyncClient() as client:
                response = await client.get(url, headers=headers)
                return response
        except Exception as e:
            print(e)

    async def verify_webhook_signature(self, payload: dict, signature: str) -> bool:
        """This function verifies the signature of a webhook payload."""
        computed_signature = hmac.new(
            PAYSTACK_SECRET_KEY.encode(), msg=payload, digestmod=hashlib.sha512
        ).hexdigest()

        return computed_signature == signature

    async def initiate_transfer(
        self,
        recipient_code: str,
        transfer_data: TransferRequest,
    ) -> TransferResponse:
        """Initiate transfer to a recipient."""
        url = f"{self.base_url}transfer"
        headers = {
            "Authorization": f"Bearer {PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        payload = {
            "source": "balance",
            "amount": transfer_data.amount * 100,  # Paystack expects amount in pesewas
            "reference": await Helpers.generate_uuid(),
            "recipient": recipient_code,
            "reason": transfer_data.reason,
        }
        print(payload)

        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=headers, json=payload)
            response_data: dict[str, Any] = response.json()
            print(response_data)

            if response.status_code != 200 or not response_data.get("status"):
                error_message = response_data.get("message", "Unknown error occurred")
                if "System Malfunction" in error_message:
                    raise PaystackSystemMalfunctionError()
                elif "account number" in error_message.lower():
                    raise PaystackAccountNumberError()
                elif "maximum amount" in error_message.lower():
                    raise PaystackMaxTransactionLimitError()
                elif "minimum amount you may send" in error_message.lower():
                    raise PaystackMinTransactionLimitError()
                elif "recipient specified is invalid" in error_message.lower():
                    raise PaystackInvalidTransferRecipientError()
                else:
                    raise PaystackError("Unexpected error", response.status_code)

            response.raise_for_status()

            return TransferResponse(**response_data)
