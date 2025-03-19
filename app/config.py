import os
from datetime import datetime, timedelta, timezone

# REDIS Configuration
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# NASA APOD API Configuration
APOD_API_URL = "https://apod.ellanan.com/api"
APOD_CACHE_TTL = 3600 # 1 hour

# NASA EONET API Configuration
DATE_TWO_WEEKS = (datetime.now(timezone.utc) - timedelta(days=14)).strftime("%Y-%m-%d")
EONET_API_URL = f"https://eonet.gsfc.nasa.gov/api/v3/events?start={DATE_TWO_WEEKS}&end=2027-12-31&status=all"
EONET_CACHE_TTL = 3600 * 6  # 6 hours