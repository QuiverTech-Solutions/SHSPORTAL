"""Validators module."""

import os

import phonenumbers
import validators
from phonenumbers import NumberParseException, geocoder


class Validators:
    """Validators class."""

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate an email address."""
        try:
            if not email:
                return False
            return validators.email(email)
        except Exception:
            return False

    @staticmethod
    def is_valid_phonenumber(phone_number: str) -> bool:
        """Validate a phone number."""
        try:
            parsed_number = phonenumbers.parse(phone_number, "GH")
            if not phonenumbers.is_valid_number(parsed_number):
                return False

            if geocoder.description_for_number(parsed_number, "en") != "Ghana":
                return False

            return True
        except NumberParseException:
            return False

    @staticmethod
    def is_image_file(file_path: str) -> bool:
        """Validate an image file"""
        image_extensions = [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".webp"]

        _, extension = os.path.splitext(file_path)

        if extension.lower() in image_extensions:
            return True
        return False
