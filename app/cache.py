import redis
import json
from app.config import REDIS_HOST, REDIS_PORT

# Redis Connection
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

def get_cached_data(key: str):
    """Retrieve cached data from Redis and ensure it's in valid JSON format."""
    cached_data = redis_client.get(key)
    if cached_data:
        try:
            return json.loads(cached_data)  # Proper JSON deserialization
        except json.JSONDecodeError:
            redis_client.delete(key)  # Remove corrupted cache
            return None
    return None

def set_cached_data(key: str, value: dict, ttl: int):
    """Store data in Redis as a JSON string with a TTL."""
    redis_client.setex(key, ttl, json.dumps(value))  # Proper JSON serialization