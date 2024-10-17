"""Settings repository module."""

from typing import List
from uuid import UUID

from databases import Database

from src.db.repositories.base import BaseRepository
from src.decorators.db import (
    handle_get_database_exceptions,
    handle_post_database_exceptions,
)
from src.errors.core import ValueError
from src.errors.database import FailedToCreateUpdateQueryError, NotFoundError
from src.models.settings import SettingsCreate, SettingsInDb, SettingsUpdate
from src.utils.helpers import Helpers

CREATE_SETTINGS_QUERY = """
INSERT INTO settings (key, value)
VALUES (:key, :value)
RETURNING id, key, value, created_at, updated_at, is_deleted
"""

GET_SETTING_BY_ID_QUERY = """
SELECT id, key, value, created_at, updated_at, is_deleted
FROM settings
WHERE id = :id AND is_deleted = FALSE
"""

GET_SETTING_BY_KEY_QUERY = """
SELECT id, key, value, created_at, updated_at, is_deleted
FROM settings
WHERE key = :key AND is_deleted = FALSE
"""

GET_SETTINGS_QUERY = """
SELECT id, key, value, created_at, updated_at, is_deleted
FROM settings
WHERE is_deleted = FALSE
"""

DELETE_SETTINGS_BY_KEY_QUERY = """
UPDATE settings
SET is_deleted = TRUE, updated_at = CURRENT_TIMESTAMP
WHERE key = :key AND is_deleted = FALSE
RETURNING id
"""


class SettingsRepository(BaseRepository):
    """Repository for managing settings."""

    def __init__(self, db: Database) -> None:
        super().__init__(db)

    @handle_post_database_exceptions("Settings")
    async def create_settings(self, *, new_settings: SettingsCreate) -> SettingsInDb:
        """Create new settings."""
        created_settings = await self.db.fetch_one(
            query=CREATE_SETTINGS_QUERY, values={**new_settings.model_dump()}
        )
        return SettingsInDb(**created_settings)

    @handle_get_database_exceptions("Settings")
    async def get_setting(self, *, id: UUID = None, key: str = None) -> SettingsInDb:
        """Get settings by key."""
        search_criteria = {
            "id": (GET_SETTING_BY_ID_QUERY, id),
            "key": (GET_SETTING_BY_KEY_QUERY, key),
        }
        for field, (query, value) in search_criteria.items():
            if value:
                settings_record = await self.db.fetch_one(
                    query=query, values={field: value}
                )
                if settings_record:
                    return SettingsInDb(**settings_record)
                else:
                    raise NotFoundError(entity_name="Settings")
        raise ValueError("Key must be provided.")

    @handle_get_database_exceptions("Settings")
    async def get_settings(
        self,
    ) -> List[SettingsInDb]:
        """Get all settings."""
        settings_records = await self.db.fetch_all(query=GET_SETTINGS_QUERY)
        return [SettingsInDb(**record) for record in settings_records]

    @handle_get_database_exceptions("Settings")
    async def update_setting(
        self, *, id: UUID, settings_update: SettingsUpdate
    ) -> SettingsInDb:
        """Update settings."""
        await self.get_setting(key=settings_update.key)

        update_fields = settings_update.model_dump(exclude_unset=True)
        if not update_fields:
            return SettingsInDb(**dict(settings_update))

        conditions = {"id": id}

        UPDATE_SETTING_QUERY = Helpers.generate_update_entity_query(
            table_name="settings",
            update_fields=update_fields,
            conditions=conditions,
        )

        if not UPDATE_SETTING_QUERY:
            raise FailedToCreateUpdateQueryError(entity_name="Settings")

        updated_setting = await self.db.fetch_one(
            query=UPDATE_SETTING_QUERY,
            values={**update_fields, "id": id},
        )

        if not updated_setting:
            raise NotFoundError(entity_name="Settings")

        return SettingsInDb(**updated_setting)

    @handle_get_database_exceptions("Settings")
    async def delete_settings_by_key(self, *, key: str) -> UUID:
        """Delete settings by key."""
        deleted_settings = await self.db.fetch_one(
            query=DELETE_SETTINGS_BY_KEY_QUERY, values={"key": key}
        )
        if deleted_settings:
            return deleted_settings["id"]
