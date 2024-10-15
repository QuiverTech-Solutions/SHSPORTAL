from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from typing import Any

from services.paystack import PaystackService 
from models.paystack import CreatePayment, VerifyTransaction, SuccessfulTransaction

paystack_router = APIRouter()

@paystack_router.post(
    "/create-payment",
    response_model=SuccessfulTransaction,
    status_code=status.HTTP_201_CREATED
)
async def create_payment(
    create_payment: CreatePayment,
    paystack_service: PaystackService = Depends(PaystackService)
) -> SuccessfulTransaction:
    """Create a payment using the Paystack API."""
    try:
        response = await paystack_service.create_payment(create_payment)
        if response.status_code == 200:
            return response.json()  
        else:
            raise HTTPException(status_code=response.status_code, detail="Payment creation failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@paystack_router.get(
    "/verify-transaction/{reference}",
    response_model=VerifyTransaction,
    status_code=status.HTTP_200_OK
)
async def verify_payment(
    reference: str,
    paystack_service: PaystackService = Depends(PaystackService)
) -> VerifyTransaction:
    """Verify a payment using the Paystack API."""
    try:
        response = await paystack_service.verify_transaction(reference)
        if response.status_code == 200:
            return response.json()  
        else:
            raise HTTPException(status_code=response.status_code, detail="Transaction verification failed")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@paystack_router.post("/webhook", status_code=status.HTTP_200_OK)
async def paystack_webhook(
    request: Request,
    paystack_service: PaystackService = Depends(PaystackService)
) -> JSONResponse:
    """Receive webhook notifications from Paystack."""
    try:
        payload = await request.body()
        signature = request.headers.get("x-paystack-signature")

        if not await paystack_service.verify_webhook_signature(payload, signature):
            raise HTTPException(status_code=400, detail="Invalid signature")

        event = await request.json()
        transaction_data = SuccessfulTransaction(**event["data"])


        return JSONResponse(content={"message": "Webhook received successfully"}, status_code=200)
    except HTTPException as e:
        return JSONResponse(content={"message": str(e)}, status_code=400)
    except Exception as e:
        return JSONResponse(content={"message": "Error processing webhook"}, status_code=500)
