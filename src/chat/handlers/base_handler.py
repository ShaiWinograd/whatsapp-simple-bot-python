"""Base message handler with common functionality."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
from ...services.service_factory import ServiceFactory
from ..conversation_manager import ConversationManager
from ...utils.text_message_builder import create_text_message as create_text_payload
from ...utils.interactive_message_builder import create_interactive_message


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

    def create_interactive_message(
        self,
        recipient: str,
        body_text: str = None,
        header_text: str = None,
        footer_text: str = None,
        buttons: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Create an interactive message payload.
        
        Args:
            recipient (str): The recipient's phone number
            body_text (str, optional): Custom body text
            header_text (str, optional): Custom header text
            footer_text (str, optional): Custom footer text
            buttons (List[Dict[str, str]], optional): Custom buttons
            
        Returns:
            Dict[str, Any]: Interactive message payload
        """
        return create_interactive_message(
            recipient=recipient,
            body_text=body_text,
            header_text=header_text,
            footer_text=footer_text,
            buttons=buttons
        )

    def create_text_message(self, recipient: str, body: str) -> Dict[str, Any]:
        """
        Create a text message payload using the text message builder.
        
        Args:
            recipient (str): The recipient's phone number
            body (str): Message text
            
        Returns:
            Dict[str, Any]: Message payload
        """
        return create_text_payload(recipient=recipient, body_text=body)

    def create_welcome_messages(self, recipient: str) -> List[Dict[str, Any]]:
        """
        Create welcome and options messages.
        
        Args:
            recipient (str): The recipient's phone number
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        # Create welcome payload using interactive handler
        from .interactive_handler import InteractiveMessageHandler
        interactive_handler = InteractiveMessageHandler(self.conversation_manager, self.service_factory)
        return [interactive_handler.create_welcome_payload(recipient)]