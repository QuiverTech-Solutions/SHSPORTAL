"""Paystack service module."""

import hashlib
import hmac

import httpx
from fastapi import HTTPException


from src.models.payment_plans import PaymentPlanInDB
from src.models.paystack import CreatePayment, CreateSubscriptionPlan
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
                create_payment.email, create_payment.telegram_id
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
                            "value": create_payment.telegram_id,
                        },
                        {
                            "display_name": "Telegram Username",
                            "variable_name": "Telegram Username",
                            "value": create_payment.telegram_username,
                        },
                        {
                            "display_name": "Questions Count",
                            "variable_name": "Questions Count",
                            "value": create_payment.questions_count,
                        },
                        {
                            "display_name": "Answers Count",
                            "variable_name": "Answers Count",
                            "value": create_payment.answers_count,
                        },
                        {
                            "display_name": "is_subscription",
                            "variable_name": "is_subscription",
                            "value": False,
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

    async def create_subscription_plan(
        self,
        create_subscription_plan: CreateSubscriptionPlan,
        payment_plan: PaymentPlanInDB,
    ) -> httpx.Response:
        """This function creates a subscription plan using the Paystack API with the specified email and amount."""
        try:
            url = f"{self.base_url}transaction/initialize"
            reference = SHSApplicationUtils.generate_transaction_id(
                create_subscription_plan.email, create_subscription_plan.telegram_id
            )
            headers = {
                "Authorization": f"Bearer {self.secret_key}",
                "Content-Type": "application/json",
            }
            data = {
                "amount": payment_plan.price
                * 100,  # paystack requires you multiply by 100.
                "email": create_subscription_plan.email,
                "currency": "GHS",
                "channels": ["mobile_money"],
                "metadata": {
                    "custom_fields": [
                        {
                            "display_name": "Telegram ID",
                            "variable_name": "Telegram ID",
                            "value": create_subscription_plan.telegram_id,
                        },
                        {
                            "display_name": "Telegram Username",
                            "variable_name": "Telegram Username",
                            "value": create_subscription_plan.telegram_username,
                        },
                        {
                            "display_name": "is_subscription",
                            "variable_name": "is_subscription",
                            "value": True,
                        },
                        {
                            "display_name": "Subscription Tier",
                            "variable_name": "Subscription Tier",
                            "value": payment_plan.name,
                        },
                        {
                            "display_name": "Balance",
                            "variable_name": "Balance",
                            "value": payment_plan.units,
                        },
                        {
                            "display_name": "Price",
                            "variable_name": "Price",
                            "value": payment_plan.price,
                        },
                        {
                            "display_name": "Payment Plan ID",
                            "variable_name": "Payment Plan ID",
                            "value": payment_plan.id,
                        },
                    ]
                },
                "reference": reference,
            }
            async with httpx.AsyncClient() as client:
                response = await client.post(url, headers=headers, json=data)
                return response

        except Exception as e:
            print(e)

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
