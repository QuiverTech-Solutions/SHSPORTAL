from fastapi import FastAPI
from routers.paystack_router import paystack_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="FastAPI Paystack Integration",
    description="An application to handle Paystack payments and transactions.",
    version="1.0.0",
)

# Configure CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(paystack_router, prefix="/api/paystack", tags=["Paystack"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Paystack Integration API!"}
