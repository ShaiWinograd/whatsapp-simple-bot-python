"""Core message processing logic for WhatsApp bot."""
from typing import Dict, Any, List
from ..utils.validators import validate_sender
from .router import MessageRouter
from .conversation_manager import ConversationManager
from ..services.service_factory import ServiceFactory


class MessageHandler:
    """Handles incoming WhatsApp messages."""

    def __init__(self, conversation_manager: ConversationManager, service_factory: ServiceFactory):
        """
        Initialize MessageHandler.
        
        Args:
            conversation_manager (ConversationManager): Manager for user conversations
            service_factory (ServiceFactory): Factory for creating service instances
        """
        self.router = MessageRouter(conversation_manager, service_factory)

    def process_message(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Process incoming WhatsApp message and return appropriate response payload.
        
        Args:
            message (Dict[str, Any]): The incoming WhatsApp message
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send or empty list if no response needed
        """
        # Validate incoming message
        if not validate_sender(message):
            return []

        # Create base payload with sender's number
        base_payload = {
            "to": message.get('from', '').strip(),
        }

        # Route message to appropriate handler
        return self.router.route_message(message, base_payload)