"""Helper functions for the project"""

import random
import re
import secrets
import time
import uuid
from datetime import datetime
from typing import Any, Dict, Optional



class Helpers:
    """Helpers class."""

    @staticmethod
    async def generate_uuid() -> str:
        """Generate uuid for user id."""
        return str(uuid.uuid4())

    @staticmethod
    async def generate_urlsafe_token() -> str:
        """Generate url safe token."""
        return secrets.token_urlsafe()

    @staticmethod
    def generate_transaction_id(phone_number: str, nominee_id: uuid.UUID) -> str:
        """Create a unique input string by combining the email and telegram ID."""
        current_time = str(time.time())
        unique_input = f"{phone_number}-{nominee_id}-{current_time}"
        namespace = uuid.NAMESPACE_OID
        unique_hash = uuid.uuid5(namespace, unique_input).hex
        allowed_id = re.sub(r"[^a-zA-Z0-9-.=]", "-", unique_hash)

        return allowed_id

    @staticmethod
    def generate_update_entity_query(
        table_name: str, update_fields: Dict[str, Any], conditions: Dict[str, Any]
    ) -> Optional[str]:
        """Dynamically construct and return an SQL UPDATE query."""
        if not update_fields:
            return None

        # Construct the SET clause dynamically
        set_clause = ", ".join(f"{key} = :{key}" for key in update_fields.keys())

        # Construct the WHERE clause dynamically
        where_clause = " AND ".join(f"{key} = :{key}" for key in conditions.keys())

        # Generate the dynamic SQL query
        update_query = f"""
        UPDATE {table_name}
        SET {set_clause}
        WHERE {where_clause} AND is_deleted = FALSE
        RETURNING *;"""

        return update_query

    # @staticmethod
    # def generate_nano_id(size: int = 12) -> str:
    #     """Generate a random string of fixed size."""
    #     return nanoid.generate(size=size)

    @staticmethod
    def generate_short_code(
        event_name: str, category_name: str, year: int = None
    ) -> str:
        """Generate a short code for a nominee."""
        event_code = event_name[:2].upper()
        category_code = category_name[:2].upper()
        year_code = str(year or datetime.now().year)[-2:]
        unique_id = f"{random.randint(0, 99):02d}"
        return f"{event_code}{category_code}{year_code}{unique_id}"
