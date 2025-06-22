"""Message handler with welcome message functionality."""
from typing import Dict, Any, List
from .message_handler_base import MessageHandlerBase
from ...utils.whatsapp_client import WhatsAppClient
from ...config.whatsapp import LABELS as WHATSAPP_LABELS


class BaseMessageHandler(MessageHandlerBase):
    """Base message handler with welcome message functionality."""

    def create_welcome_messages(self, recipient: str) -> List[Dict[str, Any]]:
        """
        Create welcome and options messages.
        
        Args:
            recipient (str): The recipient's phone number
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        # Apply bot new conversation label
        if WHATSAPP_LABELS['bot_new_conversation']:
            WhatsAppClient.apply_label(
                recipient,
                WHATSAPP_LABELS['bot_new_conversation']
            )

        # Create welcome payload using interactive handler
        from .interactive_handler import InteractiveMessageHandler
        interactive_handler = InteractiveMessageHandler(self.conversation_manager, self.service_factory)
        return [interactive_handler.create_welcome_payload(recipient)]