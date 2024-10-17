"""Dependency for db."""

# Standard library imports
import asyncio
import logging
from typing import Any, Callable, Dict, Type, Union

from databases import Database

# Third party imports
from fastapi import Depends
from starlette.requests import Request

from src.db.repositories.organization_type import OrganizationTypeRepository
from src.db.repositories.base import BaseRepository
from src.db.repositories.vote_category import VoteCategoryRepository
from src.db.repositories.vote_event import VoteEventRepository
from src.db.repositories.vote_nominee import VoteNomineeRepository
from src.db.repositories.payment_plan import PaymentPlanRepository
from src.errors.database import DatabaseError
from src.models.core import EntityValidator
from src.services.base import BaseService

app_logger = logging.getLogger("app")


def get_database(request: Request) -> Database:
    """Get Postgresql database from app state."""
    return request.app.state._db


def get_repository(repo_type: Union[Type[BaseRepository], BaseRepository]) -> Callable:
    """Dependency for db."""

    def get_repo(
        db: Database = Depends(get_database),
    ) -> Type[BaseRepository]:
        return repo_type(db)  # type: ignore

    return get_repo


def get_service(service_type: Union[Type[BaseService], BaseService]) -> Callable:
    """Dependency for services."""

    def get_service(
        repository: Database = Depends(get_repository(BaseRepository)),
    ) -> Type[BaseService]:
        return service_type(repository)  # type: ignore

    return get_service


async def validate_entities(
    request: Request, validators: Dict[str, EntityValidator]
) -> Dict[str, Any]:
    """Validate entities in request body."""
    try:
        body = await request.json()
        db = get_database(request)

        async def validate_entity(
            name: str, validator: EntityValidator
        ) -> tuple[str, Any]:
            entity_id = body.get(validator.field_name)
            if not entity_id:
                raise ValueError(f"{name} ID not found in request body")
            repo = validator.repo_type(db)
            repo_method = getattr(repo, validator.get_method)
            entity = await repo_method(id=entity_id)
            if not entity:
                raise ValueError(f"{name} not found")
            return name, entity

        tasks = [
            validate_entity(name, validator) for name, validator in validators.items()
        ]
        results = await asyncio.gather(*tasks, return_exceptions=True)

        validated_entities = {}
        for result in results:
            if isinstance(result, Exception):
                raise result
            name, entity = result
            validated_entities[name] = entity

        return validated_entities
    except DatabaseError as e:
        app_logger.exception("Database error", exc_info=e)
        raise
    except Exception as e:
        app_logger.exception("Unexpected error", exc_info=e)
        raise


def get_entity_validators(*entities: str) -> Dict[str, EntityValidator]:
    """Get entity validators for the specified entities."""
    validators = {
        "vote_nominee": EntityValidator(
            field_name="vote_nominee_id",
            repo_type=VoteNomineeRepository,
            get_method="get_vote_nominee",
        ),
        "vote_category": EntityValidator(
            field_name="category_id",
            repo_type=VoteCategoryRepository,
            get_method="get_vote_category",
        ),
        "payment_plan": EntityValidator(
            field_name="payment_plan_id",
            repo_type=PaymentPlanRepository,
            get_method="get_payment_plan",
        ),
        "vote_event": EntityValidator(
            field_name="vote_event_id",
            repo_type=VoteEventRepository,
            get_method="get_vote_event",
        ),
        "organization_type": EntityValidator(
            field_name="organization_type_id",
            repo_type=OrganizationTypeRepository,
            get_method="get_organization_type",
        ),
    }
    return {entity: validators[entity] for entity in entities}


def validate_entities_dependency(*entity_names: str) -> Callable:
    """Dependency for validating entities in request body."""

    async def validate_entities_inner(
        request: Request,
        validators: Dict[str, EntityValidator] = Depends(
            lambda: get_entity_validators(*entity_names)
        ),
    ) -> Dict[str, Any]:
        return await validate_entities(request, validators)

    return validate_entities_inner
