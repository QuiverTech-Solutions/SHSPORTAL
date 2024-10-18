"""Route to accept user payments."""

from decimal import Decimal
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from src.errors.paystack import PaystackError
from src.models.paystack.charge import ChargeOTPVerifyRequest, ChargeResponse
from src.models.paystack.payment import CreateVotingUSSDPayment
from src.models.paystack.transaction import SuccessfulTransaction
from src.services.paystack import PaystackService
from src.db.repositories import payment, admin_wallet, transactions, schools_wallet
from src.api.dependencies.database import get_repository


paystack_router = APIRouter()


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
        print(e)
        raise
    except Exception as e:
        print(e)
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
        print(e)
        raise
    except HTTPException as e:
        print(e)
        raise HTTPException(status_code=400, detail="Invalid details") from e
    except Exception as e:
        print(e)
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
        if paystack_event_type.startswith("charge"):  # User completed a ussd prompt
            transaction_data = SuccessfulTransaction(**event["data"])

            custom_fields = {
                field.variable_name: field.value
                for field in transaction_data.metadata.custom_fields
            }

            student_name = custom_fields.get("Student Name", "")
            school_name = custom_fields.get("School Name", "")
            school_id = UUID(custom_fields.get("School ID", ""))
            total_amount = Decimal(custom_fields.get("Amount paid", ""))
            school_amount = Decimal(custom_fields.get("School amount", ""))
            admin_amount = Decimal(custom_fields.get("Admin amount", ""))
            phone_number = custom_fields.get("Phone Number", "")

            print(
                student_name,
                school_name,
                school_id,
                total_amount,
                school_amount,
                admin_amount,
                phone_number,
            )


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
        print(e)
        return JSONResponse(
            content={"message": "Error processing transaction"}, status_code=200
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"message": "Error processing transaction"}, status_code=500
        )


@paystack_router.post("/webhook", status_code=status.HTTP_200_OK)
async def paystack_webhook(
    request: Request,
    paystack_service: PaystackService = Depends(PaystackService),
    payment_repo: payment = Depends(get_repository(payment)),
    school_wallet_repo: schools_wallet = Depends(get_repository(schools_wallet)),
    admin_wallet_repo: admin_wallet = Depends(get_repository(admin_wallet)),
    transaction_repo: transactions = Depends(get_repository(transactions)),
) -> JSONResponse:
    """This function creates a webhook, that'll receive a response from Paystack."""
    try:
        payload = await request.body()
        signature = request.headers.get("x-paystack-signature")

        if not await paystack_service.verify_webhook_signature(payload, signature):
            raise HTTPException(status_code=400, detail="Invalid signature")  # noqa

        event = await request.json()
        paystack_event_type = event["event"]
        
        if paystack_event_type.startswith("charge"):  # User completed a ussd prompt
            transaction_data = SuccessfulTransaction(**event["data"])

            custom_fields = {
                field.variable_name: field.value
                for field in transaction_data.metadata.custom_fields
            }

            student_name = custom_fields.get("Student Name", "")
            school_name = custom_fields.get("School Name", "")
            school_id = UUID(custom_fields.get("School ID", ""))
            total_amount = Decimal(custom_fields.get("Amount paid", ""))
            school_amount = Decimal(custom_fields.get("School amount", ""))
            admin_amount = Decimal(custom_fields.get("Admin amount", ""))
            phone_number = custom_fields.get("Phone Number", "")

            # Process the payment, update wallet balances and record the transaction
            async with transaction_repo.TransactionUpdate:  # Start a DB transaction
                # Insert payment details into the payment table
                await payment.PaymentCreate(
                    student_name=student_name,
                    school_name=school_name,
                    total_amount=total_amount,
                    phone_number=phone_number,
                )

                # Update the school’s wallet balance
                await school_wallet_repo.SchoolWalletUpdate(
                    school_id=school_id,
                    amount=school_amount
                )

                # Update the admin’s wallet balance
                await admin_wallet_repo.update_wallet_balance(
                    amount=admin_amount
                )

                # Insert the transaction details into the transaction table
                await transaction_repo.TransactionCreate(
                    school_id=school_id,
                    total_amount=total_amount,
                    school_amount=school_amount,
                    admin_amount=admin_amount,
                )

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
        print(e)
        return JSONResponse(
            content={"message": "Error processing transaction"}, status_code=200
        )
    except Exception as e:
        print(e)
        return JSONResponse(
            content={"message": "Error processing transaction"}, status_code=500
        )