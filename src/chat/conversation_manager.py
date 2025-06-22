from datetime import datetime, timedelta
from typing import Dict, Optional

from ..services.base_service import BaseConversationService
from ..utils.whatsapp_client import WhatsAppClient
from ..config.responses import WHATSAPP_LABELS

class ConversationManager:
    def __init__(self, timeout_minutes: int = 300): # Default timeout of 300 minutes (5 hours)
        self.conversations: Dict[str, BaseConversationService] = {}
        self.last_activity: Dict[str, datetime] = {}
        self.timeout_minutes = timeout_minutes
    
    def add_conversation(self, user_id: str, service: BaseConversationService) -> None:
        """Add a new conversation service for a user.
        If the user already has an active conversation, it will be replaced.
        Args:
            user_id (str): Unique identifier for the user
            service (BaseConversationService): The conversation service instance
        """
        self.conversations[user_id] = service
        self.last_activity[user_id] = datetime.now()
        
        # Apply labels for new conversation
        # Apply bot new conversation label
        if WHATSAPP_LABELS['bot_new_conversation']:
            WhatsAppClient.apply_label(
                user_id,
                WHATSAPP_LABELS['bot_new_conversation']
            )
    
    def get_conversation(self, user_id: str) -> Optional[BaseConversationService]:
        """Retrieve the conversation service for a user if it exists and is active.
        Args:
            user_id (str): Unique identifier for the user
        Returns:
            Optional[BaseConversationService]: The conversation service instance if active, None otherwise
        """
        if self.is_conversation_active(user_id):
            self.last_activity[user_id] = datetime.now()
            return self.conversations.get(user_id)
        return None
    
    def is_conversation_active(self, user_id: str) -> bool:
        """Check if a user has an active conversation that hasn't timed out.
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            bool: True if the user has an active conversation, False otherwise
        """
        if user_id not in self.conversations:
            return False
            
        current_time = datetime.now()
        last_active = self.last_activity.get(user_id)
        
        if not last_active:
            return False
            
        return (current_time - last_active) <= timedelta(minutes=self.timeout_minutes)

    def cleanup_stale_conversations(self) -> None:
        """Remove conversations that have been inactive for longer than the timeout period."""
        current_time = datetime.now()
        stale_users = [
            user_id for user_id, last_active in self.last_activity.items()
            if (current_time - last_active) > timedelta(minutes=self.timeout_minutes)
        ]
        for user_id in stale_users:
            self.conversations.pop(user_id, None)
            self.last_activity.pop(user_id, None)
            
    def remove_conversation(self, user_id: str) -> None:
        """Remove a conversation for a specific user.
        
        Args:
            user_id (str): Unique identifier for the user
        """
        self.conversations.pop(user_id, None)
        self.last_activity.pop(user_id, None)