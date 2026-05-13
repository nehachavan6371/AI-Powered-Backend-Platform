"""LLM Service Tests"""

import pytest
from unittest.mock import AsyncMock, patch
from services.llm_service import LLMService


@pytest.mark.asyncio
async def test_generate_response():
    """Test response generation"""
    service = LLMService()
    with patch.object(service.chat, 'invoke', return_value=AsyncMock(content="Test response")):
        response = await service.generate_response("Test prompt")
        assert isinstance(response, str)


@pytest.mark.asyncio
async def test_count_tokens():
    """Test token counting"""
    service = LLMService()
    text = "This is a test sentence."
    count = await service.count_tokens(text)
    assert count > 0


@pytest.mark.asyncio
async def test_calculate_cost():
    """Test cost calculation"""
    service = LLMService()
    cost = await service.calculate_cost(100, 50)
    assert cost > 0


@pytest.mark.asyncio
async def test_error_handling():
    """Test error handling"""
    service = LLMService()
    # Should handle errors gracefully
    response = await service.error_handler.handle_llm_error(Exception("Test error"))
    assert isinstance(response, str)
