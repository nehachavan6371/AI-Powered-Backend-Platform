"""Error Handling Tests"""

import pytest
from services.error_handler import ErrorHandler


@pytest.mark.asyncio
async def test_llm_error_handling():
    """Test LLM error handling"""
    handler = ErrorHandler()
    response = await handler.handle_llm_error(Exception("Test error"))
    assert isinstance(response, str)
    assert len(response) > 0


@pytest.mark.asyncio
async def test_database_error_handling():
    """Test database error handling"""
    handler = ErrorHandler()
    response = await handler.handle_database_error(Exception("DB error"))
    assert isinstance(response, dict)
    assert "error" in response


@pytest.mark.asyncio
async def test_input_validation():
    """Test input validation"""
    handler = ErrorHandler()
    data = {"name": "test", "value": 123}
    result = handler.validate_input(data, ["name", "value"])
    assert result is True


@pytest.mark.asyncio
async def test_input_validation_failure():
    """Test input validation failure"""
    handler = ErrorHandler()
    data = {"name": "test"}
    result = handler.validate_input(data, ["name", "missing_field"])
    assert result is False
