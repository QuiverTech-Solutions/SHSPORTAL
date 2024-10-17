"""Decorator for get db operations to handle database exceptions."""

from functools import wraps
from typing import Any

from asyncpg import (
    DataError,
    ForeignKeyViolationError,
    PostgresError,
    UniqueViolationError,
)

from src.errors.core import InternalServerError, InvalidTokenError
from src.errors.database import (
    AlreadyExistsError,
    BadRequestError,
    DataTypeError,
    ForeignKeyError,
    GeneralDatabaseError,
    IncorrectCredentialsError,
    NotFoundError,
)


def handle_get_database_exceptions(entity_name: str) -> callable:
    """Decorator to handle database exceptions for get operations."""

    def decorator(func: callable) -> callable:
        @wraps(func)
        async def wrapper(
            self, *args: tuple, **kwargs: dict[str, Any]  # noqa
        ) -> callable:
            try:
                return await func(self, *args, **kwargs)
            except DataError as e:
                print(f"DataError for {entity_name}", exc_info=True)
                raise DataTypeError(entity_name=entity_name) from e
            except PostgresError as e:
                print(f"PostgresError for {entity_name}", exc_info=True)
                raise GeneralDatabaseError(entity_name=entity_name) from e
            except ValueError as e:
                print(f"ValueError for {entity_name}", exc_info=True)
                raise BadRequestError(
                    f"Bad Request: Invalid details for {entity_name}"
                ) from e
            except NotFoundError:
                print(f"NotFoundError for {entity_name}")
                raise
            except IncorrectCredentialsError:
                print(f"Incorrect credentials for {entity_name}")
                raise
            except InvalidTokenError:
                print(f"Invalid jwt token for {entity_name}")
                raise
            except Exception as e:
                print(f"Unexpected error for {entity_name}", exc_info=True)
                raise InternalServerError(
                    additional_message="Unexpected error. Try again."
                ) from e

        return wrapper

    return decorator


def handle_post_database_exceptions(
    entity_name: str, foreign_key_entity: str = None, already_exists_entity: str = None
) -> callable:
    """Decorator to handle database exceptions for post operations."""

    def decorator(func: callable) -> callable:

        @wraps(func)
        async def wrapper(
            self, *args: tuple, **kwargs: dict[str, Any]  # noqa
        ) -> callable:
            try:
                return await func(self, *args, **kwargs)
            except UniqueViolationError as e:
                print(f"UniqueViolationError for {entity_name}", exc_info=True)
                if "email" in str(e):
                    raise AlreadyExistsError(entity_name="Email") from e
                elif "referral_code" in str(e):
                    raise AlreadyExistsError(entity_name="Referral Code") from e
                else:
                    raise AlreadyExistsError(entity_name=already_exists_entity) from e
            except ForeignKeyViolationError as e:
                print(f"ForeignKeyViolationError for {entity_name}", exc_info=True)
                raise ForeignKeyError(entity_name=foreign_key_entity) from e
            except DataError as e:
                print(f"DataError for {entity_name}", exc_info=True)
                raise DataTypeError(entity_name=entity_name) from e
            except PostgresError as e:
                print(f"PostgresError for {entity_name}", exc_info=True)
                raise GeneralDatabaseError(entity_name=entity_name) from e
            except NotFoundError:
                print(f"NotFoundError for {entity_name}")
                raise
            except IncorrectCredentialsError:
                print(f"Incorrect credentials for {entity_name}")
                raise
            except InvalidTokenError:
                print(f"Invalid jwt token for {entity_name}")
                raise
            except Exception as e:
                print(f"Unexpected error for {entity_name}", exc_info=True)
                raise InternalServerError(
                    additional_message="Unexpected error. Try again."
                ) from e

        return wrapper

    return decorator
