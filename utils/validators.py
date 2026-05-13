"""Input/Output Validators"""

import re
from typing import Any, List


class InputValidator:
    """Validate input data"""

    @staticmethod
    def validate_query(query: str) -> bool:
        """Validate query string"""
        if not query or len(query) < 2:
            return False
        if len(query) > 1000:
            return False
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email address"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    @staticmethod
    def sanitize_string(text: str) -> str:
        """Sanitize string input"""
        # Remove special characters
        text = re.sub(r'[<>"\']', '', text)
        return text.strip()


class OutputValidator:
    """Validate output data"""

    @staticmethod
    def validate_response(response: Any) -> bool:
        """Validate response structure"""
        if isinstance(response, dict):
            return len(response) > 0
        elif isinstance(response, str):
            return len(response) > 0
        return True
