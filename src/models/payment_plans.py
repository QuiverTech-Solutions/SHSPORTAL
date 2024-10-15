"""Payment plans Model."""

from src.models.base import (
    CoreModel,
    DateTimeModelMixin,
    IDModelMixin,
    UpdatedAtModelMixin,
)


class PaymentPlanBase(CoreModel):
    """All common characteristics of payment plans."""

    name: str
    price: float
    units: int


class PaymentPlanCreate(PaymentPlanBase, UpdatedAtModelMixin):
    """Creating a new payment plan."""

    pass


class PaymentPlanUpdate(PaymentPlanCreate):
    """Updating a payment plan."""

    is_active: bool


class PaymentPlanInDB(PaymentPlanCreate, IDModelMixin, DateTimeModelMixin):
    """Payment plan coming in from DB."""

    is_active: bool


class PaymentPlanPublic(
    IDModelMixin, PaymentPlanCreate, DateTimeModelMixin, UpdatedAtModelMixin
):
    """Payment plan to be returned to the client."""

    is_active: bool
