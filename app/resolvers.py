import httpx
import strawberry
import json
from typing import List
from app.cache import get_cached_data, set_cached_data
from app.config import APOD_API_URL, APOD_CACHE_TTL
from app.config import EONET_API_URL, EONET_CACHE_TTL
from app.schemas import PictureOfTheDay
from app.schemas import NaturalDisaster, EventCategory, EventSource, EventGeometry

@strawberry.type
class Query:
    @strawberry.field
    async def natural_disasters(self) -> List[NaturalDisaster]:
        """Fetches recent natural disasters from NASA's EONET API, with Redis caching."""

        # Check Redis cache first
        cached_data = get_cached_data("nasa:eonet_events")
        if cached_data:
            print("Returning cached EONET data")
            return [
                NaturalDisaster(
                    id=event["id"],
                    title=event["title"],
                    description=event.get("description"),
                    link=event["link"],
                    closed=event.get("closed"),
                    categories=[EventCategory(**cat) for cat in event["categories"]],
                    sources=[EventSource(**src) for src in event["sources"]], 
                    geometry=[
                        EventGeometry(
                            id=geo.get("id", geo["date"]), 
                            magnitudeValue=geo.get("magnitudeValue"),
                            magnitudeUnit=geo.get("magnitudeUnit"),
                            date=geo["date"],
                            type=geo["type"],
                            coordinates=geo["coordinates"]
                        ) for geo in event["geometry"]
                    ],
                )
                for event in cached_data
            ]

        # Fetch from EONET API
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(EONET_API_URL)
                response.raise_for_status()
                data = response.json()
        except httpx.ReadTimeout:
            print("EONET API request timed out!")
            return []
        except httpx.RequestError as e:
            print(f"Failed to reach EONET API: {e}")
            return []
        
        # Transform API response
        events = [
            {
                "id": event["id"],
                "title": event["title"],
                "description": event.get("description"),
                "link": event["link"],
                "closed": event.get("closed"),
                "categories": [cat for cat in event["categories"]],
                "sources": [src for src in event["sources"]],
                "geometry": [geo for geo in event["geometry"]]
            }
            for event in data.get("events", [])
        ]

        # Store in Redis cache
        set_cached_data("nasa:eonet_events", events, EONET_CACHE_TTL)

        return [
            NaturalDisaster(
                id=event["id"],
                title=event["title"],
                description=event.get("description"),
                link=event["link"],
                closed=event.get("closed"),
                categories=[EventCategory(**cat) for cat in event["categories"]],  
                sources=[EventSource(**src) for src in event["sources"]], 
                geometry=[
                    EventGeometry(
                        id=geo.get("id", geo["date"]), 
                        magnitudeValue=geo.get("magnitudeValue"),
                        magnitudeUnit=geo.get("magnitudeUnit"),
                        date=geo["date"],
                        type=geo["type"],
                        coordinates=geo["coordinates"]
                    ) for geo in event["geometry"]
                ],
            )
            for event in events
        ]
    
    @strawberry.field
    async def picture_of_the_day(self) -> PictureOfTheDay:
        """Fetches NASA's Picture of the Day, with Redis caching."""
        
        # Check Redis cache first
        cached_data = get_cached_data("nasa:picture_of_the_day")
        if cached_data:
            print("Returning cached Picture of the Day data")
            return PictureOfTheDay(**cached_data)

        # Fetch from NASA API
        async with httpx.AsyncClient() as client:
            response = await client.get(APOD_API_URL)
            data = response.json()

        # Store in Redis cache
        set_cached_data("nasa:picture_of_the_day", data, APOD_CACHE_TTL)

        return PictureOfTheDay(**data)
