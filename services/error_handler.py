"""Error Handling Service"""

import logging
from typing import Optional
import asyncio

logger = logging.getLogger(__name__)


class ErrorHandler:
    """Error handling with fallbacks and recovery"""

    async def handle_llm_error(self, error: Exception) -> str:
        """Handle LLM errors with fallback"""
        logger.error(f"LLM error: {error}")
        
        # Fallback response
        return (
            "I encountered an issue processing your request. "
            "Please try again or rephrase your query."
        )

    async def handle_database_error(self, error: Exception) -> dict:
        """Handle database errors"""
        logger.error(f"Database error: {error}")
        return {
            "error": "Database error",
            "message": "Failed to process request. Please try again later."
        }

    async def retry_with_backoff(self, func, max_retries: int = 3):
        """Retry function with exponential backoff"""
        for attempt in range(max_retries):
            try:
                return await func()
            except Exception as exc:
                if attempt == max_retries - 1:
                    raise
                wait_time = 2 ** attempt
                logger.warning(f"Attempt {attempt + 1} failed. Retrying in {wait_time}s...")
                await asyncio.sleep(wait_time)

    def validate_input(self, data: dict, required_fields: list) -> bool:
        """Validate input data"""
        for field in required_fields:
            if field not in data or not data[field]:
                logger.error(f"Missing required field: {field}")
                return False
        return True
