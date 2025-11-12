import json
from typing import Any, Optional


def safe_json_loads(json_str: Optional[str]) -> Optional[dict]:
    """Safely parse JSON string to dict, returning None if invalid or empty."""
    if not json_str:
        return None
    
    try:
        return json.loads(json_str)
    except (json.JSONDecodeError, TypeError):
        return None


def safe_json_dumps(data: Any) -> Optional[str]:
    """Safely convert data to JSON string, returning None if conversion fails."""
    if data is None:
        return None
    
    try:
        return json.dumps(data)
    except (TypeError, ValueError):
        return None