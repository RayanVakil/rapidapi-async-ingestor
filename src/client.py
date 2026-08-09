import asyncio
import logging
from typing import Dict, Any, Optional
import httpx

logger = logging.getLogger(__name__)

class MaxRetriesExceededError(Exception):
    """Exception raised when the maximum number of retries is exceeded for an API request."""
    pass

class AsyncCarAPIClient:
    """Asynchronous client for RapidAPI Car API v2 with exponential backoff retries."""
    
    def __init__(self, api_key: str):
        self.base_url = "https://car-api2.p.rapidapi.com"
        self.headers = {
            "x-rapidapi-key": api_key,
            "x-rapidapi-host": "car-api2.p.rapidapi.com"
        }
        # 15 second timeout to handle API latency
        self.client = httpx.AsyncClient(base_url=self.base_url, headers=self.headers, timeout=15.0)

    async def close(self):
        """Gracefully close the underlying HTTP client."""
        await self.client.aclose()

    async def __aenter__(self):
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def _request_with_retry(self, endpoint: str, params: Optional[Dict[str, Any]] = None, max_retries: int = 4) -> Dict[str, Any]:
        """
        Executes a GET request with exponential backoff for rate limits (429) and network/server errors.
        """
        for attempt in range(max_retries):
            try:
                response = await self.client.get(endpoint, params=params)
                
                # Handle Rate Limiting
                if response.status_code == 429:
                    wait_time = 2 ** attempt
                    logger.warning(f"Rate limited on {endpoint}. Retrying in {wait_time}s... (Attempt {attempt + 1}/{max_retries})")
                    await asyncio.sleep(wait_time)
                    continue
                    
                response.raise_for_status()
                return response.json()
                
            except httpx.RequestError as e:
                logger.error(f"Network error on {endpoint}: {e}. Attempt {attempt + 1}/{max_retries}")
                if attempt == max_retries - 1:
                    break
                await asyncio.sleep(2 ** attempt)
                
            except httpx.HTTPStatusError as e:
                # Retry on 5xx Server Errors
                if e.response.status_code >= 500:
                    logger.error(f"Server error {e.response.status_code} on {endpoint}. Attempt {attempt + 1}/{max_retries}")
                    if attempt == max_retries - 1:
                        break
                    await asyncio.sleep(2 ** attempt)
                else:
                    # Do not retry on 4xx Client Errors (except 429 handled above)
                    raise
                    
        # If the loop exhausts without returning, raise our custom exception
        raise MaxRetriesExceededError(f"Failed to fetch {endpoint} after {max_retries} attempts.")

    async def get_exterior_colors(self, make: str, model: str, year: int) -> Dict[str, Any]:
        return await self._request_with_retry("/api/exterior-colors", params={"make": make, "model": model, "year": year})

    async def get_years(self, make: str, model: str) -> Dict[str, Any]:
        return await self._request_with_retry("/api/years", params={"make": make, "model": model})

    async def get_bodies(self, make: str, model: str, year: int) -> Dict[str, Any]:
        return await self._request_with_retry("/api/bodies", params={"make": make, "model": model, "year": year})

    async def get_mileage(self, vehicle_id: int) -> Dict[str, Any]:
        # Utilizing query params for the collection endpoint
        return await self._request_with_retry("/api/mileages", params={"make_model_trim_id": vehicle_id, "verbose": "yes"})
