"""Image message handler implementation."""
from typing import Dict, Any, List
from .base_handler import BaseMessageHandler


class ImageMessageHandler(BaseMessageHandler):
    """Handler for image messages."""

    def handle(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle image message type and return appropriate response.
        
        Args:
            message (Dict[str, Any]): The incoming WhatsApp message
            base_payload (Dict[str, Any]): Base payload for response message
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        recipient = base_payload["to"]

        # Check for existing conversation first
        conversation = self.conversation_manager.get_conversation(recipient)
        if conversation:
            try:
                # Get response from service and ensure we return it
                response = conversation.handle_response(message)
                if response:
                    return response
            except Exception as e:
                print(f"ERROR handling image in conversation: {e}")
                # Just return empty list on error, let service handle retries
                return []


        # If no active conversation, show the welcome message
        # Images without context should start a new conversation
        return self.create_welcome_messages(recipient)