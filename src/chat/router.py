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
        try:
            command_type = message.get('type', '').strip().lower()
            
            handler = self.handlers.get(command_type)
            if handler:
                try:
                    return handler.handle(message, base_payload)
                except Exception as e:
                    print(f"Error in handler for type {command_type}: {str(e)}")
                    return [TextMessageHandler(
                        self.handlers['text'].conversation_manager,
                        self.handlers['text'].service_factory
                    ).create_text_message(base_payload["to"], "מצטערים, אירעה שגיאה. נא נסו שוב.")]
            
            print(f"Unhandled message type: {command_type}")
            return [TextMessageHandler(
                self.handlers['text'].conversation_manager,
                self.handlers['text'].service_factory
            ).create_text_message(base_payload["to"], "סוג ההודעה אינו נתמך כרגע")]
            
        except Exception as e:
            print(f"Error routing message: {str(e)}")
            return [TextMessageHandler(
                self.handlers['text'].conversation_manager,
                self.handlers['text'].service_factory
            ).create_text_message(base_payload["to"], "מצטערים, אירעה שגיאה. נא נסו שוב.")]