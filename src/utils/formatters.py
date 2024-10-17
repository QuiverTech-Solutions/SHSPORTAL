"""Formatters module."""

import datetime
import os
import re
import secrets

from fastapi import UploadFile


class Formatters:
    """Formatters class"""

    @staticmethod
    def format_ghanaian_number_with_plus(phone_number: str) -> str:
        """Format Ghanaian phone number."""
        if phone_number.startswith("+233"):
            return phone_number
        elif len(phone_number) == 9:
            return "+233" + phone_number
        elif phone_number.startswith("0"):
            return "+233" + phone_number[1:]
        else:
            return "+" + phone_number

    @staticmethod
    def format_database_url(db_url: str) -> str:
        """Removes '+asyncpg' from the database URL if present."""
        if "+asyncpg" in db_url:
            modified_url = db_url.replace("+asyncpg", "")
            return modified_url
        else:
            # Return the original URL if '+asyncpg' is not found
            return db_url

    @staticmethod
    def format_image_file(file: UploadFile) -> str:
        """Format an image file name."""
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        unique_id = secrets.token_hex(2)
        _, file_extension = os.path.splitext(file.filename)
        new_file_name = f"{current_date}{unique_id}{file_extension}"
        return new_file_name

    @staticmethod
    def replace_whitespace_with_underscore(text: str) -> str:
        """Remove special characters from a string."""
        return re.sub(r"\s+", "_", text)

    @staticmethod
    def modify_database_url(db_url: str) -> str:
        """Removes '+asyncpg' from the database URL if present."""
        if "+asyncpg" in db_url:
            modified_url = db_url.replace("+asyncpg", "")
            return modified_url
        else:
            # Return the original URL if '+asyncpg' is not found
            return db_url
