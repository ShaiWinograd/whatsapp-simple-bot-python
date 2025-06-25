"""Welcome message handler implementation."""
from typing import Dict, Any, List

from ...models.message_payload import MessagePayloadBuilder
from ...config.responses.common import WELCOME, NAVIGATION

class WelcomeHandler:
    """Handles initial welcome messages and service selection."""
    
    def __init__(self, conversation_manager, flow_factory):
        """Initialize WelcomeHandler with required dependencies.
        
        Args:
            conversation_manager: The conversation manager instance
            flow_factory: The flow factory instance
        """
        self._conversation_manager = conversation_manager
        self._flow_factory = flow_factory

    def create_welcome_payload(self, recipient: str) -> Dict[str, Any]:
        """Create welcome message with service selection buttons
        
        Args:
            recipient (str): The recipient's phone number
            
        Returns:
            Dict[str, Any]: Welcome message payload
        """
        return MessagePayloadBuilder.create_interactive_message(
            recipient=recipient,
            body_text=WELCOME['message'],
            header_text=WELCOME['header'],
            buttons=[
                {"id": "moving", "title": WELCOME['moving_button']},
                {"id": "organization", "title": WELCOME['organization_button']},
                {"id": "other", "title": WELCOME['other_button']},
                {"id": "help", "title": NAVIGATION['talk_to_representative']}
            ]
        )

    def handle_welcome(self, recipient: str) -> List[Dict[str, Any]]:
        """Handle initial welcome for a user
        
        Args:
            recipient (str): The recipient's phone number
            
        Returns:
            List[Dict[str, Any]]: List containing welcome message payload
        """
        return [self.create_welcome_payload(recipient)]