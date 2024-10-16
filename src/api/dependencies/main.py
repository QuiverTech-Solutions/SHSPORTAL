from fastapi import FastAPI
from routes.paystack_router import paystack_router
from fastapi.middleware.cors import CORSMiddleware

from utils.databse import engine  # Note the corrected import for 'database'
from db.repositories.db_model import Base  # Ensure you import Base correctly
from routes.crud_router import crud_router
app = FastAPI(
    title="FastAPI Paystack Integration",
    description="An application to handle Paystack payments and transactions.",
    version="1.0.0",
)

# Configure CORS 
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to your frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the Paystack router
app.include_router(paystack_router, prefix="/api/paystack", tags=["Paystack"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI Paystack Integration API!"}

# Create the database tables
Base.metadata.create_all(bind=engine)

app.include_router(crud_router, prefix="/api", tags=["CRUD Operations"])  