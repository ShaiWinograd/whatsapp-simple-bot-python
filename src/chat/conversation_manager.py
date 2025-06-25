from typing import Optional, Dict, Any, List

from ..business.flows.abstract_business_flow import AbstractBusinessFlow as BusinessFlow
from ..business.flow_factory import BusinessFlowFactory
from .state_manager import StateManager
from ..whatsapp.label_manager import LabelManager
from .timeout_manager import TimeoutManager
from .business_flow_manager import BusinessFlowManager
from ..models.message_payload import MessagePayloadBuilder
from ..config.responses.common import WELCOME

class ConversationManager:
    """Main coordinator for all conversation-related operations"""
    
    def __init__(self, timeout_minutes: int = 300):
        self._state_manager = StateManager()
        self._label_manager = LabelManager()
        self._timeout_manager = TimeoutManager(timeout_minutes)
        self._business_flow_manager = BusinessFlowManager(self._state_manager, self._label_manager)
        
    def start_conversation(self, user_id: str, flow_type: str) -> None:
        """Start a new conversation with a specific business flow
        
        Args:
            user_id (str): Unique identifier for the user
            flow_type (str): Type of business flow to start
        """
        flow = BusinessFlowFactory.create_flow(flow_type)
        if flow:
            self._label_manager.remove_all_labels(user_id)
            self._state_manager.set_state(user_id, flow)
            self._timeout_manager.update_activity(user_id)
            self._label_manager.apply_label(user_id, 'bot_new_conversation')
        
    def get_conversation(self, user_id: str) -> Optional[BusinessFlow]:
        """Retrieve the business flow for a user if active
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            Optional[BusinessFlow]: The business flow if active
        """
        if self._timeout_manager.is_active(user_id):
            self._timeout_manager.update_activity(user_id)
            return self._state_manager.get_state(user_id)
        return None
        
    def remove_conversation(self, user_id: str) -> None:
        """Remove a conversation for a user
        
        Args:
            user_id (str): Unique identifier for the user
        """
        self._label_manager.remove_all_labels(user_id)
        self._state_manager.remove_state(user_id)
        self._timeout_manager.remove_activity(user_id)
        
    def cleanup_stale_conversations(self) -> None:
        """Remove conversations that have timed out"""
        for user_id in self._timeout_manager.get_stale_users():
            self.remove_conversation(user_id)
            
    def handle_support_request(self, user_id: str) -> None:
        """Handle a support request
        
        Args:
            user_id (str): Unique identifier for the user
        """
        self._business_flow_manager.handle_support_request(user_id)
        
    def update_conversation_state(self, user_id: str, new_state: str) -> None:
        """Update conversation state
        
        Args:
            user_id (str): Unique identifier for the user
            new_state (str): New state to set
        """
        self._business_flow_manager.handle_state_transition(user_id, new_state)
        
    def handle_user_input(self, user_id: str, user_input: str) -> Optional[str]:
        """Handle user input for active conversation
        
        Args:
            user_id (str): Unique identifier for the user
            user_input (str): Input from user
            
        Returns:
            Optional[str]: Response message if conversation exists
        """
        flow = self.get_conversation(user_id)
        if flow:
            next_state = flow.handle_input(user_input)
            self.update_conversation_state(user_id, next_state)
            return flow.get_next_message()
        # No active conversation, return welcome message
        welcome_msg = MessagePayloadBuilder.create_interactive_message(
            recipient=user_id,
            body_text=WELCOME['message'],
            buttons=[
                {"id": "moving", "title": WELCOME['moving_button']},
                {"id": "organization", "title": WELCOME['organization_button']}
            ]
        )
        return welcome_msg