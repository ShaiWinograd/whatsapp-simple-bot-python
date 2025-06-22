"""Text message handler implementation."""
from typing import Dict, Any, List
from .base_handler import BaseMessageHandler


class TextMessageHandler(BaseMessageHandler):
    """Handler for text messages."""

    def handle(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle text message type and return appropriate response.
        
        Args:
            message (Dict[str, Any]): The incoming WhatsApp message
            base_payload (Dict[str, Any]): Base payload for response message
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        recipient = base_payload["to"]

        # Check for existing conversation first
        conversation_response = self.check_existing_conversation(recipient, message)
        if conversation_response is not None:
            return conversation_response

        # For any other text message, show the welcome message
        return self.create_welcome_messages(recipient)