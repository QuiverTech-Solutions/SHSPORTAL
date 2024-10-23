"""Setting up configs."""

from databases import DatabaseURL
from starlette.config import Config
from starlette.datastructures import Secret

config = Config(".env")

# Project configs
PROJECT_NAME = "SHSPORTAL"
VERSION = "1.0"
API_PREFIX = "/api/v1"

# Environment
ENV = config("ENV", cast=str, default="DEV")

# Database[Sqlite3]
if ENV == "DEV":
    DATABASE_URL = config(
        "DATABASE_URL",
        cast=DatabaseURL,
        default="",
    )
else:
    DATABASE_URL = config(
        "PROD_DATABASE_URL",
        cast=DatabaseURL,
        default="",
    )

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES = config(
    "ACCESS_TOKEN_EXPIRE_MINUTES", cast=int, default=60
)
REFRESH_TOKEN_EXPIRE_DAYS = config("REFRESH_TOKEN_EXPIRE_DAYS", cast=int, default=7)
SECRET_KEY = config("SECRET_KEY", cast=str, default="")
ALGORITHM = config("ALGORITHM", cast=str, default="HS256")

# Paystack
PAYSTACK_ENV = config("PAYSTACK_ENV", cast=str)
PAYSTACK_BASE_URL = config("PAYSTACK_BASE_URL", cast=str)
if PAYSTACK_ENV == "PROD":
    PAYSTACK_PUBLIC_KEY = config("PAYSTACK_LIVE_PUBLIC_KEY")
    PAYSTACK_SECRET_KEY = config("PAYSTACK_LIVE_SECRET_KEY")
else:
    PAYSTACK_PUBLIC_KEY = config("PAYSTACK_TEST_PUBLIC_KEY")
    PAYSTACK_SECRET_KEY = config("PAYSTACK_TEST_SECRET_KEY")

# AWS S3 configs
S3_BUCKET_NAME = config("S3_BUCKET_NAME", cast=str, default="")
S3_ACCESS_KEY_ID = config("S3_ACCESS_KEY_ID", cast=str, default="")
S3_SECRET_ACCESS_KEY = config("S3_SECRET_ACCESS_KEY", cast=Secret, default="")
S3_REGION = config("S3_REGION", cast=str, default="")

# SMTP
SMTP_HOST = config("SMTP_HOST", cast=str, default="")
SMTP_PORT = config("SMTP_PORT", cast=int, default=0)
SMTP_USERNAME = config("SMTP_USERNAME", cast=str, default="")
SMTP_PASSWORD = config("SMTP_PASSWORD", cast=Secret, default="")

# Sendgrid
SENDGRID_API_KEY = config("SENDGRID_API_KEY", cast=str, default="")

# MailerSend
MAILERSEND_API_KEY = config("MAILERSEND_API_KEY", cast=str, default="")

# MailGun
MAILGUN_API_KEY = config("MAILGUN_API_KEY", cast=str, default="")
MAILGUN_API_URL = config("MAILGUN_API_URL", cast=str, default="")

# Secret Key
SECRET_KEY=config("SECRET_KEY", cast=str, default="")