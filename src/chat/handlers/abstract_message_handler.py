"""Abstract message handler with common functionality."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from ...business.flow_factory import BusinessFlowFactory
from ...business.flows.abstract_business_flow import AbstractBusinessFlow
from ..conversation_manager import ConversationManager
from ...utils.text_message_builder import create_text_message as create_text_payload
from ...utils.interactive_message_builder import InteractiveMessageBuilder


class AbstractMessageHandler(ABC):
    """Abstract base class for message handlers."""

    def __init__(self, conversation_manager: ConversationManager, flow_factory: BusinessFlowFactory):
        """Initialize base handler
        
        Args:
            conversation_manager (ConversationManager): Manager for user conversations
            flow_factory (BusinessFlowFactory): Factory for creating business flow instances
        """
        self._conversation_manager = conversation_manager
        self._flow_factory = flow_factory

    @abstractmethod
    def handle(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle a specific message type
        
        Args:
            message (Dict[str, Any]): The incoming message
            base_payload (Dict[str, Any]): Base payload for response
            
        Returns:
            List[Dict[str, Any]]: List of response payloads
        """
        pass

    def check_existing_conversation(self, recipient: str, message: Dict[str, Any]) -> Optional[List[Dict[str, Any]]]:
        """Check if there's an existing conversation and handle the message
        
        Args:
            recipient (str): The recipient's phone number
            message (Dict[str, Any]): The incoming message
            
        Returns:
            Optional[List[Dict[str, Any]]]: Response payloads if conversation exists, None otherwise
        """
        flow = self._conversation_manager.get_conversation(recipient)
        if flow:
            # Handle the input using the flow
            next_state = flow.handle_input(message)
            # Update the flow state
            self._conversation_manager.update_conversation_state(recipient, next_state)
            # Get the next message to send
            next_message = flow.get_next_message()
            if next_message:
                return [self.create_flow_message(recipient, next_message)]
        return None

    def create_flow_message(self, recipient: str, message: str) -> Dict[str, Any]:
        """Create appropriate message type based on content
        
        Args:
            recipient (str): The recipient's phone number
            message (str): Message content from flow
            
        Returns:
            Dict[str, Any]: Message payload
        """
        # If message contains button definitions, create interactive message
        if "buttons" in message:
            return InteractiveMessageBuilder.create_message(recipient=recipient, **message)
        # Otherwise create text message
        return create_text_payload(recipient=recipient, body_text=message)

    def create_interactive_message(
        self,
        recipient: str,
        body_text: str = None,
        header_text: str = None,
        footer_text: str = None,
        buttons: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Create an interactive message payload
        
        Args:
            recipient (str): The recipient's phone number
            body_text (str, optional): Custom body text
            header_text (str, optional): Custom header text
            footer_text (str, optional): Custom footer text
            buttons (List[Dict[str, str]], optional): Custom buttons
            
        Returns:
            Dict[str, Any]: Interactive message payload
        """
        return InteractiveMessageBuilder.create_message(
            recipient=recipient,
            body_text=body_text,
            header_text=header_text,
            footer_text=footer_text,
            buttons=buttons
        )

    def create_text_message(self, recipient: str, body: str) -> Dict[str, Any]:
        """Create a text message payload using the text message builder
        
        Args:
            recipient (str): The recipient's phone number
            body (str): Message text
            
        Returns:
            Dict[str, Any]: Message payload
        """
        return create_text_payload(recipient=recipient, body_text=body)

    def create_welcome_messages(self, recipient: str) -> List[Dict[str, Any]]:
        """Create welcome and options messages
        
        Args:
            recipient (str): The recipient's phone number
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        # Create welcome payload using interactive handler
        from .interactive_handler import InteractiveMessageHandler
        interactive_handler = InteractiveMessageHandler(self._conversation_manager, self._flow_factory)
        return [interactive_handler.create_welcome_payload(recipient)]