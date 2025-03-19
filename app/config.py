import os

# NASA API Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
NASA_CACHE_TTL = 3600 # 1 hour
NASA_API_URL = "https://apod.ellanan.com/api"