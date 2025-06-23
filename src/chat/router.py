"""Message routing functionality."""
from typing import Dict, Any, List
from .handlers import TextMessageHandler, InteractiveMessageHandler, ImageMessageHandler, VideoMessageHandler
from ..services.service_factory import ServiceFactory
from .conversation_manager import ConversationManager


class MessageRouter:
    """Routes messages to appropriate handlers based on message type."""

    def __init__(self, conversation_manager: ConversationManager, service_factory: ServiceFactory):
        self.handlers = {
            'text': TextMessageHandler(conversation_manager, service_factory),
            'interactive': InteractiveMessageHandler(conversation_manager, service_factory),
            'reply': InteractiveMessageHandler(conversation_manager, service_factory),
            'image': ImageMessageHandler(conversation_manager, service_factory),
            'video': VideoMessageHandler(conversation_manager, service_factory)
        }
        
    def route_message(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Route message to appropriate handler based on message type.
        
        Args:
            message (Dict[str, Any]): The incoming message
            base_payload (Dict[str, Any]): Base payload for response
            
        Returns:
            List[Dict[str, Any]]: List of response payloads
        """
        command_type = message.get('type', '').strip().lower()
        
        handler = self.handlers.get(command_type)
        if handler:
            return handler.handle(message, base_payload)
            
        print(f"Unhandled message type: {command_type}")
        return []