"""LLM Service - OpenAI Integration"""

import logging
import asyncio
from typing import Optional, AsyncGenerator
import openai
from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from app.config import get_settings
from services.error_handler import ErrorHandler

logger = logging.getLogger(__name__)
settings = get_settings()


class LLMService:
    """LLM Service for OpenAI integration"""

    def __init__(self):
        """Initialize LLM service"""
        openai.api_key = settings.openai_api_key
        self.model = settings.openai_model
        self.embedding_model = settings.openai_embedding_model
        self.temperature = settings.openai_temperature
        self.max_tokens = settings.openai_max_tokens
        self.error_handler = ErrorHandler()
        self.chat = ChatOpenAI(
            model_name=self.model,
            temperature=self.temperature,
            max_tokens=self.max_tokens
        )

    async def generate_response(self, prompt: str, context: Optional[str] = None) -> str:
        """Generate response from LLM"""
        try:
            full_prompt = f"{context}\n{prompt}" if context else prompt
            response = await asyncio.to_thread(
                self.chat.invoke,
                full_prompt
            )
            return response.content
        except Exception as exc:
            logger.error(f"Error generating response: {exc}")
            return await self.error_handler.handle_llm_error(exc)

    async def stream_response(self, prompt: str, context: Optional[str] = None) -> AsyncGenerator[str, None]:
        """Stream response from LLM"""
        try:
            full_prompt = f"{context}\n{prompt}" if context else prompt
            async for chunk in self._stream_from_llm(full_prompt):
                yield chunk
        except Exception as exc:
            logger.error(f"Error streaming response: {exc}")
            yield await self.error_handler.handle_llm_error(exc)

    async def _stream_from_llm(self, prompt: str) -> AsyncGenerator[str, None]:
        """Internal streaming from LLM"""
        callbacks = [StreamingStdOutCallbackHandler()]
        response = await asyncio.to_thread(
            self.chat.invoke,
            prompt,
            callbacks=callbacks
        )
        yield response.content

    async def count_tokens(self, text: str) -> int:
        """Count tokens in text"""
        try:
            encoding = await asyncio.to_thread(
                self._get_encoding
            )
            tokens = encoding.encode(text)
            return len(tokens)
        except Exception as exc:
            logger.error(f"Error counting tokens: {exc}")
            return len(text.split())  # Fallback to word count

    @staticmethod
    def _get_encoding():
        """Get token encoding"""
        import tiktoken
        return tiktoken.encoding_for_model(settings.openai_model)

    async def calculate_cost(self, prompt_tokens: int, completion_tokens: int) -> float:
        """Calculate API cost"""
        # Pricing as of knowledge cutoff (adjust as needed)
        prompt_cost = 0.00003  # $0.03 per 1K tokens
        completion_cost = 0.00006  # $0.06 per 1K tokens
        
        total_cost = (prompt_tokens * prompt_cost + completion_tokens * completion_cost) / 1000
        return total_cost

    async def generate_embedding(self, text: str) -> list:
        """Generate embedding for text"""
        try:
            response = await asyncio.to_thread(
                openai.Embedding.create,
                input=text,
                model=self.embedding_model
            )
            return response['data'][0]['embedding']
        except Exception as exc:
            logger.error(f"Error generating embedding: {exc}")
            raise
