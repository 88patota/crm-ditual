from enum import Enum
from pydantic import BaseModel
from datetime import datetime
from typing import Any, Dict


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