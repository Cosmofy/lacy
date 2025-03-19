import strawberry
from typing import List, Optional

# NASA APOD
@strawberry.type
class PictureOfTheDay:
    title: str
    url: str
    explanation: str
    date: str

# NASA EONET
@strawberry.type
class EventCategory:
    id: str
    title: str

@strawberry.type
class EventSource:
    id: str
    url: str

@strawberry.type
class EventGeometry:
    id: str  # Using date as unique identifier
    magnitudeValue: Optional[float] = None
    magnitudeUnit: Optional[str] = None
    date: str
    type: str
    coordinates: List[float]

@strawberry.type
class NaturalDisaster:
    id: str
    title: str
    description: Optional[str]
    link: str
    closed: Optional[str]
    categories: List[EventCategory]
    sources: List[EventSource]
    geometry: List[EventGeometry]