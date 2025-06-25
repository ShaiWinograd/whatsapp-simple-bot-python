"""Welcome message handler implementation."""
from typing import Dict, Any, List
from ...models.message_payload import MessagePayloadBuilder
from ...config.responses.common import WELCOME

class WelcomeHandler:
    """Handles initial welcome messages and service selection."""

    @staticmethod
    def create_welcome_payload(recipient: str) -> Dict[str, Any]:
        """Create welcome message with service selection buttons
        
        Args:
            recipient (str): The recipient's phone number
            
        Returns:
            Dict[str, Any]: Welcome message payload
        """
        return MessagePayloadBuilder.create_message(
            recipient=recipient,
            body_text=WELCOME['message'],
            buttons=[
                {"id": "moving", "title": WELCOME['moving_button']},
                {"id": "organization", "title": WELCOME['organization_button']}
            ]
        )

    @staticmethod
    def handle_welcome(recipient: str) -> List[Dict[str, Any]]:
        """Handle initial welcome for a user
        
        Args:
            recipient (str): The recipient's phone number
            
        Returns:
            List[Dict[str, Any]]: List containing welcome message payload
        """
        return [WelcomeHandler.create_welcome_payload(recipient)]