from datetime import datetime, timedelta
from typing import Dict, Optional, List

from ..services.base_service import BaseConversationService
from ..utils.whatsapp_client import WhatsAppClient
from ..config.whatsapp import LABELS

class ConversationManager:
    def __init__(self, timeout_minutes: int = 300): # Default timeout of 300 minutes (5 hours)
        self.conversations: Dict[str, BaseConversationService] = {}
        self.last_activity: Dict[str, datetime] = {}
        self.timeout_minutes = timeout_minutes
        self.user_labels: Dict[str, List[str]] = {}
    
    def add_conversation(self, user_id: str, service: BaseConversationService) -> None:
        """Add a new conversation service for a user.
        If the user already has an active conversation, it will be replaced.
        Args:
            user_id (str): Unique identifier for the user
            service (BaseConversationService): The conversation service instance
        """
        # Remove all existing labels
        self.remove_all_labels(user_id)
        
        self.conversations[user_id] = service
        self.last_activity[user_id] = datetime.now()
        self.user_labels[user_id] = []
        
        # Add new conversation label
        self.apply_label(user_id, 'bot_new_conversation')
    
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
            self.remove_conversation(user_id)
            
    def remove_conversation(self, user_id: str) -> None:
        """Remove a conversation for a specific user.
        
        Args:
            user_id (str): Unique identifier for the user
        """
        self.remove_all_labels(user_id)
        self.conversations.pop(user_id, None)
        self.last_activity.pop(user_id, None)
        self.user_labels.pop(user_id, None)

    def handle_support_request(self, user_id: str) -> None:
        """Handle a support request by updating labels.
        
        Args:
            user_id (str): Unique identifier for the user
        """
        self.remove_all_labels(user_id)
        self.apply_label(user_id, 'waiting_urgent_support')
        
    def apply_label(self, user_id: str, label_key: str) -> None:
        """Apply a label to a conversation.
        
        Args:
            user_id (str): Unique identifier for the user
            label_key (str): Key of the label to apply from LABELS dict
        """
        if label_key in LABELS and LABELS[label_key]:
            WhatsAppClient.apply_label(user_id, LABELS[label_key])
            if user_id not in self.user_labels:
                self.user_labels[user_id] = []
            if label_key not in self.user_labels[user_id]:
                self.user_labels[user_id].append(label_key)
                
    def remove_label(self, user_id: str, label_key: str) -> None:
        """Remove a label from a conversation.
        
        Args:
            user_id (str): Unique identifier for the user
            label_key (str): Key of the label to remove from LABELS dict
        """
        if label_key in LABELS and LABELS[label_key]:
            WhatsAppClient.remove_label(user_id, LABELS[label_key])
            if user_id in self.user_labels:
                self.user_labels[user_id] = [l for l in self.user_labels[user_id] if l != label_key]
                
    def remove_all_labels(self, user_id: str) -> None:
        """Remove all labels from a conversation.
        
        Args:
            user_id (str): Unique identifier for the user
        """
        if user_id in self.user_labels:
            for label in self.user_labels[user_id]:
                self.remove_label(user_id, label)
            
    def update_service_state(self, user_id: str, new_state: str) -> None:
        """Update conversation state and manage associated labels.
        
        Args:
            user_id (str): Unique identifier for the user
            new_state (str): New state to set
        """
        service = self.get_conversation(user_id)
        if not service:
            return
            
        service.set_conversation_state(new_state)
        
        # Update labels based on state
        if new_state == 'initial':
            self.remove_all_labels(user_id)
            self.apply_label(user_id, 'bot_new_conversation')
            
        elif new_state == 'awaiting_emergency_support':
            self.apply_label(user_id, 'waiting_urgent_support')
            
        elif new_state == 'completed':
            self.apply_label(user_id, 'waiting_call_before_quote')
            
        # Apply service-specific labels
        service_type = service.get_service_name().lower()
        if service_type in ['moving', 'organization']:
            self.apply_label(user_id, service_type)