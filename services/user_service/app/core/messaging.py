import redis.asyncio as redis
from typing import Optional, Any
import json
import logging
from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Dict
from app.core.config import settings

logger = logging.getLogger(__name__)


class EventType(str, Enum):
    USER_CREATED = "user.created"
    USER_UPDATED = "user.updated"
    USER_DELETED = "user.deleted"
    USER_LOGIN = "user.login"


class BaseEvent(BaseModel):
    event_type: EventType
    timestamp: datetime
    service: str
    data: Dict[str, Any]


class UserCreatedEvent(BaseEvent):
    event_type: EventType = EventType.USER_CREATED
    
    def __init__(self, user_data: dict, **kwargs):
        super().__init__(
            timestamp=datetime.utcnow(),
            service="user_service",
            data=user_data,
            **kwargs
        )


class UserUpdatedEvent(BaseEvent):
    event_type: EventType = EventType.USER_UPDATED
    
    def __init__(self, user_data: dict, **kwargs):
        super().__init__(
            timestamp=datetime.utcnow(),
            service="user_service",
            data=user_data,
            **kwargs
        )


class UserDeletedEvent(BaseEvent):
    event_type: EventType = EventType.USER_DELETED
    
    def __init__(self, user_id: int, **kwargs):
        super().__init__(
            timestamp=datetime.utcnow(),
            service="user_service",
            data={"user_id": user_id},
            **kwargs
        )


class UserLoginEvent(BaseEvent):
    event_type: EventType = EventType.USER_LOGIN
    
    def __init__(self, user_data: dict, **kwargs):
        super().__init__(
            timestamp=datetime.utcnow(),
            service="user_service",
            data=user_data,
            **kwargs
        )


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
            message_str = json.dumps(message, default=str)
            await self.redis_client.publish(channel, message_str)
            logger.info(f"Published message to channel {channel}")
        except Exception as e:
            logger.error(f"Failed to publish message: {e}")
            raise


# Global Redis client instance
redis_client = RedisClient(settings.redis_url)


async def publish_user_created(user_data: dict):
    """Publish user created event"""
    try:
        event = UserCreatedEvent(user_data=user_data)
        await redis_client.publish("user_events", event.model_dump())
        logger.info(f"Published user created event for user {user_data.get('id')}")
    except Exception as e:
        logger.error(f"Failed to publish user created event: {e}")


async def publish_user_updated(user_data: dict):
    """Publish user updated event"""
    try:
        event = UserUpdatedEvent(user_data=user_data)
        await redis_client.publish("user_events", event.model_dump())
        logger.info(f"Published user updated event for user {user_data.get('id')}")
    except Exception as e:
        logger.error(f"Failed to publish user updated event: {e}")


async def publish_user_deleted(user_id: int):
    """Publish user deleted event"""
    try:
        event = UserDeletedEvent(user_id=user_id)
        await redis_client.publish("user_events", event.model_dump())
        logger.info(f"Published user deleted event for user {user_id}")
    except Exception as e:
        logger.error(f"Failed to publish user deleted event: {e}")


async def publish_user_login(user_data: dict):
    """Publish user login event"""
    try:
        event = UserLoginEvent(user_data=user_data)
        await redis_client.publish("user_events", event.model_dump())
        logger.info(f"Published user login event for user {user_data.get('id')}")
    except Exception as e:
        logger.error(f"Failed to publish user login event: {e}")


async def initialize_messaging():
    """Initialize messaging connection"""
    await redis_client.connect()


async def close_messaging():
    """Close messaging connection"""
    await redis_client.disconnect()