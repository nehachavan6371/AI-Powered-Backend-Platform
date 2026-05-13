"""API Gateway Service - External API Integration"""

import logging
import asyncio
from typing import Optional, Any
import aiohttp
from tenacity import retry, stop_after_attempt, wait_exponential

logger = logging.getLogger(__name__)


class APIGateway:
    """API Gateway for external API integration"""

    def __init__(self, base_url: str, timeout: int = 30):
        """Initialize API gateway"""
        self.base_url = base_url
        self.timeout = timeout
        self.session = None

    async def __aenter__(self):
        """Context manager entry"""
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        if self.session:
            await self.session.close()

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def get(self, endpoint: str, **kwargs) -> Optional[dict]:
        """GET request with retry"""
        try:
            url = f"{self.base_url}/{endpoint}"
            async with self.session.get(url, timeout=self.timeout, **kwargs) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    logger.error(f"GET {url} returned {response.status}")
                    return None
        except asyncio.TimeoutError:
            logger.error(f"GET request to {url} timed out")
            raise
        except Exception as exc:
            logger.error(f"Error in GET request: {exc}")
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    async def post(self, endpoint: str, data: dict, **kwargs) -> Optional[dict]:
        """POST request with retry"""
        try:
            url = f"{self.base_url}/{endpoint}"
            async with self.session.post(url, json=data, timeout=self.timeout, **kwargs) as response:
                if response.status in [200, 201]:
                    return await response.json()
                else:
                    logger.error(f"POST {url} returned {response.status}")
                    return None
        except Exception as exc:
            logger.error(f"Error in POST request: {exc}")
            raise
