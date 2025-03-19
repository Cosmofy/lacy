import strawberry

@strawberry.type
class PictureOfTheDay:
    title: str
    url: str
    explanation: str
    date: str