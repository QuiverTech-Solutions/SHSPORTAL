"""Route configuration for the application."""

from fastapi import FastAPI

from src.core.config import DATABASE_URL


def setup_routes(app: FastAPI) -> None:
    """Configure all application routes."""
    from src.api.routes.admin_wallet import admin_wallet_router
    from src.api.routes.crud_router import crud_router
    from src.api.routes.payment import payment_router
    from src.api.routes.paystack import paystack_router
    from src.api.routes.role import role_router
    from src.api.routes.schools import school_router
    from src.api.routes.schools_wallet import school_wallet_router
    from src.api.routes.settings import settings_router
    from src.api.routes.students import student_router
    from src.api.routes.super_admin_wallet import super_admin_wallet_router
    from src.api.routes.transactions import transaction_router
    from src.api.routes.user_role import user_roles_router
    from src.api.routes.users import users_router

    app.include_router(crud_router, prefix="/crud", tags=["CRUD"])
    app.include_router(school_router, prefix="/schools", tags=["Schools"])
    app.include_router(paystack_router, prefix="/paystack", tags=["Paystack"])
    app.include_router(users_router, prefix="/users", tags=["users"])
    app.include_router(payment_router, prefix="/payment", tags=["payment"])
    app.include_router(role_router, prefix="/role", tags=["role"])
    app.include_router(
        school_wallet_router, prefix="/school_wallet", tags=["school_wallet"]
    )
    app.include_router(school_router, prefix="/school_router", tags=["school_router"])
    app.include_router(settings_router, prefix="/settings", tags=["settings"])
    app.include_router(student_router, prefix="/student", tags=["student"])
    app.include_router(
        super_admin_wallet_router,
        prefix="/super_admin_wallet",
        tags=["super_admin_wallet"],
    )
    app.include_router(transaction_router, prefix="/transaction", tags=["transaction"])
    app.include_router(user_roles_router, prefix="/user_roles", tags=["user_roles"])
    app.include_router(
        admin_wallet_router, prefix="/admin_wallet", tags=["admin_wallet"]
    )

    @app.get("/", name="index")
    async def index() -> str:
        return f"This i s the database  url {str(DATABASE_URL)}"
        return "Visit ip_addrESs:8000/docs or localhost8000/docs to view documentation."
