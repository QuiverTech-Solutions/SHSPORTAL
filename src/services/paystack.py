"""Paystack service module."""

import hashlib
import hmac

import httpx
from fastapi import HTTPException


from src.models.paystack import CreatePayment
from src.services.utils import SHSApplicationUtils


class PaystackService:
    """A class to handle Paystack API requests."""

    def __init__(self) -> None:
        self.base_url = "PAYSTACK_BASE_URL"
        self.secret_key = "PAYSTACK_SECRET_KEY"

    async def create_payment(
        self,
        create_payment: CreatePayment,
        amount: float,
    ) -> httpx.Response:
        """This function creates a mobile money payment transaction using the Paystack API with the specified email and amount."""
        if amount <= 0:
            raise HTTPException(status_code=400, detail="Amount must be greater than 0")
        try:
            url = f"{self.base_url}transaction/initialize"
            reference = SHSApplicationUtils.generate_transaction_id(
                create_payment.email, create_payment.student_id
            )
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json",
            }

            data = {
                "amount": amount * 100,
                "email": create_payment.email,
                "currency": "GHS",
                "channels": ["mobile_money"],
                "metadata": {
                    "custom_fields": [
                        {
                            "display_name": "Telegram ID",
                            "variable_name": "Telegram ID",
                            "value": create_payment.student_id,
                        },
                        {
                            "display_name": "Student ID",
                            "variable_name": "Student name",
                            "value": create_payment.name,
                        },
                       
                    ]
                },
                "reference": reference,
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                return response
        except Exception as e:
            print("An exception occurred", e)

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
            "PAYSTACK_SECRET_KEY".encode(), msg=payload, digestmod=hashlib.sha512
        ).hexdigest()

        return computed_signature == signature
