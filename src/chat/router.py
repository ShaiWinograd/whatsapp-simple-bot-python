"""Message routing functionality."""
from typing import Dict, Any, List
from .handlers import TextMessageHandler, InteractiveMessageHandler, ImageMessageHandler, VideoMessageHandler
from ..business.flow_factory import BusinessFlowFactory
from .conversation_manager import ConversationManager
from ..config.responses.common import GENERAL


class MessageRouter:
    """Routes messages to appropriate handlers based on message type."""

    def __init__(self, conversation_manager: ConversationManager, flow_factory: BusinessFlowFactory):
        """Initialize MessageRouter
        
        Args:
            conversation_manager (ConversationManager): Manager for user conversations
            flow_factory (BusinessFlowFactory): Factory for creating business flow instances
        """
        self._conversation_manager = conversation_manager
        self._flow_factory = flow_factory
        
        # Initialize handlers with new business flow factory
        self.handlers = {
            'text': TextMessageHandler(conversation_manager, flow_factory),
            'interactive': InteractiveMessageHandler(conversation_manager, flow_factory),
            'reply': InteractiveMessageHandler(conversation_manager, flow_factory),
            'image': ImageMessageHandler(conversation_manager, flow_factory),
            'video': VideoMessageHandler(conversation_manager, flow_factory)
        }
        
    def route_message(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Route message to appropriate handler based on message type.
        
        Args:
            message (Dict[str, Any]): The incoming message
            base_payload (Dict[str, Any]): Base payload for response
            
        Returns:
            List[Dict[str, Any]]: List of response payloads
        """
        try:
            # Get message type and find appropriate handler
            message_type = message.get('type', '').strip().lower()
            handler = self.handlers.get(message_type)
            
            if handler:
                try:
                    return handler.handle(message, base_payload)
                except Exception as e:
                    print(f"Error in handler for type {message_type}: {str(e)}")
                    return self._create_error_response(base_payload["to"], GENERAL['error'])
            
            print(f"Unhandled message type: {message_type}")
            return self._create_error_response(base_payload["to"], 
                "סוג ההודעה אינו נתמך כרגע")
            
        except Exception as e:
            print(f"Error routing message: {str(e)}")
            return self._create_error_response(base_payload["to"], GENERAL['error'])
            
    def _create_error_response(self, recipient: str, message: str) -> List[Dict[str, Any]]:
        """Create error response message
        
        Args:
            recipient (str): Message recipient
            message (str): Error message
            
        Returns:
            List[Dict[str, Any]]: List containing error message payload
        """
        return [TextMessageHandler(
            self._conversation_manager,
            self._flow_factory
        ).create_text_message(recipient, message)]