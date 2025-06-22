"""Base message handler class."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ...services.service_factory import ServiceFactory
from ..conversation_manager import ConversationManager
from ...utils.whatsapp_client import WhatsAppClient
from ...config.responses import WHATSAPP_LABELS


class BaseMessageHandler(ABC):
    """Abstract base class for message handlers."""

    def __init__(self, conversation_manager: ConversationManager, service_factory: ServiceFactory):
        self.conversation_manager = conversation_manager
        self.service_factory = service_factory

    @abstractmethod
    def handle(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle a specific message type.

        Args:
            message (Dict[str, Any]): The incoming message
            base_payload (Dict[str, Any]): Base payload for response

        Returns:
            List[Dict[str, Any]]: List of response payloads
        """
        pass

    def check_existing_conversation(self, recipient: str, message: Dict[str, Any]) -> List[Dict[str, Any]] | None:
        """
        Check if there's an existing conversation and handle the message.

        Args:
            recipient (str): The recipient's phone number
            message (Dict[str, Any]): The incoming message

        Returns:
            List[Dict[str, Any]] | None: Response payloads if conversation exists, None otherwise
        """
        service = self.conversation_manager.get_conversation(recipient)
        if service:
            return service.handle_response(message)
        return None

    @staticmethod
    def create_welcome_messages(recipient: str) -> List[Dict[str, Any]]:
        """
        Create welcome and options messages.
        
        Args:
            recipient (str): The recipient's phone number
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        from ...models.webhook_payload import InteractiveMessagePayload
        from ...config.responses import RESPONSES

        # Apply bot new conversation label
        if WHATSAPP_LABELS['bot_new_conversation']:
            WhatsAppClient.apply_label(
                recipient,
                WHATSAPP_LABELS['bot_new_conversation']
            )

        options_message = InteractiveMessagePayload(
            to=recipient,
            body=RESPONSES['welcome_message'],
            button_messages=RESPONSES['options']
        ).to_dict()
        
        return [options_message]