import redis.asyncio as redis
from typing import Optional, Any
import json
import logging

logger = logging.getLogger(__name__)


class RedisClient:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis_client: Optional[redis.Redis] = None
    
    async def connect(self):
        """Connect to Redis"""
        try:
            self.redis_client = redis.from_url(self.redis_url)
            await self.redis_client.ping()
            logger.info("Connected to Redis successfully")
        except Exception as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise
    
    async def disconnect(self):
        """Disconnect from Redis"""
        if self.redis_client:
            await self.redis_client.close()
            logger.info("Disconnected from Redis")
    
    async def publish(self, channel: str, message: dict):
        """Publish message to a channel"""
        if not self.redis_client:
            raise RuntimeError("Redis client not connected")
        
        try:
            message_str = json.dumps(message)
            await self.redis_client.publish(channel, message_str)
            logger.info(f"Published message to channel {channel}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise
    
    async def subscribe(self, channel: str):
        """Subscribe to a channel"""
        if not self.redis_client:
            raise RuntimeError("Redis client not connected")
        
        pubsub = self.redis_client.pubsub()
        await pubsub.subscribe(channel)
        return pubsub
    
    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        """Set a key-value pair with optional expiration"""
        if not self.redis_client:
            raise RuntimeError("Redis client not connected")
        
        value_str = json.dumps(value) if not isinstance(value, str) else value
        await self.redis_client.set(key, value_str, ex=expire)
    
    async def get(self, key: str) -> Optional[Any]:
        """Get value by key"""
        if not self.redis_client:
            raise RuntimeError("Redis client not connected")
        
        value = await self.redis_client.get(key)
        if value:
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value.decode('utf-8')
        return None
    
    async def delete(self, key: str):
        """Delete a key"""
        if not self.redis_client:
            raise RuntimeError("Redis client not connected")
        
        await self.redis_client.delete(key)