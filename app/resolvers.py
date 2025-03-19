import httpx
import strawberry
from app.cache import get_cached_data, set_cached_data
from app.config import NASA_API_URL, NASA_CACHE_TTL
from app.schemas import PictureOfTheDay

@strawberry.type
class Query:
    @strawberry.field
    async def picture_of_the_day(self) -> PictureOfTheDay:
        """Fetches NASA's Picture of the Day, with Redis caching."""
        
        # Check Redis cache first
        picture_data = get_cached_data("nasa:picture_of_the_day")
        if picture_data:
            print("Returning cached data")
            return PictureOfTheDay(**picture_data)

        # Fetch from NASA API
        async with httpx.AsyncClient() as client:
            response = await client.get(NASA_API_URL)
            data = response.json()

        # Prepare structured response
        picture_data = {
            "title": data["title"],
            "url": data["url"],
            "explanation": data["explanation"],
            "date": data["date"],
        }

        # Store in Redis cache
        set_cached_data("nasa:picture_of_the_day", picture_data, NASA_CACHE_TTL)

        return PictureOfTheDay(**picture_data)