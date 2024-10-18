"""Route to accept user payments."""

from decimal import Decimal
import logging
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from fastapi.responses import JSONResponse

from models.paystack.payment import CreateVotingUSSDPayment
from src.api.dependencies.auth import get_event_org_admin, get_super_admin
from src.api.dependencies.database import get_repository
from src.db.repositories.payment_plan import PaymentPlanRepository

from src.enums.paystack import AvailableBankCountries
from src.errors.paystack import PaystackError
from src.models.paystack.bank import (
    BankAccountVerificationResponse,
    RetrieveBanksResponse,
)
from src.models.paystack.charge import ChargeOTPVerifyRequest, ChargeResponse
from src.models.paystack.transaction import SuccessfulTransaction
from src.models.paystack.transfer import TransferWebhookData
from src.services.paystack import PaystackService

paystack_router = APIRouter()
audit_logger = logging.getLogger("audit")


@paystack_router.post(
    "/ussd",
    response_model=ChargeResponse,
    status_code=status.HTTP_200_OK,
)
async def initiate_ussd_payment(
    create_payment: CreateVotingUSSDPayment,
    paystack_service: PaystackService = Depends(PaystackService),
) -> ChargeResponse:
    """This function creates a ussd mobile money amount."""
    try:
        value = await paystack_service.create_ussd_payment(create_payment)
        return value
    except HTTPException as e:
        audit_logger.exception(exc_info=e)
        raise
    except Exception as e:
        audit_logger.exception(exc_info=e)
        raise HTTPException(status_code=500, detail="Internal Server Error") from e


@paystack_router.post(
    "/ussd/otp",
    response_model=ChargeResponse,
    status_code=status.HTTP_200_OK,
)
async def verify_ussd_otp(
    otp_data: ChargeOTPVerifyRequest,
    paystack_service: PaystackService = Depends(PaystackService),
) -> ChargeResponse:
    """This function verifies a ussd mobile money amount."""
    try:
        return await paystack_service.verify_ussd_otp_payment(otp_data=otp_data)
    except PaystackError as e:
        audit_logger.exception("Paystack error", exc_info=e)
        raise
    except HTTPException as e:
        audit_logger.exception(exc_info=e)
        raise HTTPException(status_code=400, detail="Invalid details") from e
    except Exception as e:
        audit_logger.exception(exc_info=e)
        raise HTTPException(
            status_code=500, detail="Unexpected error. Please try again."
        ) from e


@paystack_router.post("/webhook", status_code=status.HTTP_200_OK)
async def paystack_webhook(
    request: Request,
    paystack_service: PaystackService = Depends(PaystackService),
) -> JSONResponse:
    """This function creates a webhook, that'll receive a response from Paystack."""
    try:
        payload = await request.body()
        signature = request.headers.get("x-paystack-signature")

        if not await paystack_service.verify_webhook_signature(payload, signature):
            raise HTTPException(status_code=400, detail="Invalid signature")  # noqa

        event = await request.json()
        paystack_event_type = event["event"]
        audit_logger.info("Paystack event type: %s", paystack_event_type)
        if paystack_event_type.startswith("charge"):  # User completed a ussd prompt
            transaction_data = SuccessfulTransaction(**event["data"])

            custom_fields = {
                field.variable_name: field.value
                for field in transaction_data.metadata.custom_fields
            }

            student_name = custom_fields.get("Student Name", "")
            school_name = custom_fields.get("School Name", "")
            school_id = UUID(custom_fields.get("School ID", ""))
            total_amount  = Decimal(custom_fields.get("Amount paid", ""))
            school_amount = Decimal(custom_fields.get("School amount", ""))
            admin_amount = Decimal(custom_fields.get("Admin amount", ""))
            phone_number = custom_fields.get("Phone Number", "")

            # TODO: Now with this,  add it to the payment, wallet, and transaction tables
            
            audit_logger.info("Done updating charge event")
            return JSONResponse(
                content={"message": "Transaction Payment processed successfully"},
                status_code=200,
            )
        else:
            return JSONResponse(
                content={"message": "Invalid Webhook event"},
                status_code=200,
            )
    except HTTPException as e:
        audit_logger.exception("HTTPException", exc_info=e)
        return JSONResponse(
            content={"message": "Error processing transaction"}, status_code=200
        )
    except Exception as e:
        audit_logger.exception("System Exception", exc_info=e)
        return JSONResponse(
            content={"message": "Error processing transaction"}, status_code=500
        )
