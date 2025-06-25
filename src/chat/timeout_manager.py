from datetime import datetime, timedelta
from typing import Dict, Optional

class TimeoutManager:
    """Responsible for managing conversation timeouts"""
    
    def __init__(self, timeout_minutes: int = 300):  # Default timeout of 300 minutes (5 hours)
        self._last_activity: Dict[str, datetime] = {}
        self._timeout_minutes = timeout_minutes
        
    def update_activity(self, user_id: str) -> None:
        """Update the last activity time for a user
        
        Args:
            user_id (str): Unique identifier for the user
        """
        self._last_activity[user_id] = datetime.now()
        
    def is_active(self, user_id: str) -> bool:
        """Check if a conversation is still active (not timed out)
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            bool: True if the conversation is active, False otherwise
        """
        last_active = self._last_activity.get(user_id)
        if not last_active:
            return False
            
        current_time = datetime.now()
        return (current_time - last_active) <= timedelta(minutes=self._timeout_minutes)
        
    def remove_activity(self, user_id: str) -> None:
        """Remove activity tracking for a user
        
        Args:
            user_id (str): Unique identifier for the user
        """
        self._last_activity.pop(user_id, None)
        
    def get_stale_users(self) -> list[str]:
        """Get list of users with stale conversations
        
        Returns:
            list[str]: List of user IDs with stale conversations
        """
        current_time = datetime.now()
        return [
            user_id for user_id, last_active in self._last_activity.items()
            if (current_time - last_active) > timedelta(minutes=self._timeout_minutes)
        ]