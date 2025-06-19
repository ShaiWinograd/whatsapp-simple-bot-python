"""Base service class for handling conversation flows."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any

from src.utils.whatsapp_client import WhatsAppClient
from webhook_payload import TextMessagePayload


class BaseConversationService(ABC):
    """Base class for handling specific conversation flows."""
    
    def __init__(self, recipient: str):
        """
        Initialize the service.
        
        Args:
            recipient (str): The recipient's phone number
        """
        self.recipient = recipient
        self.conversation_state = "initial"
    
    @abstractmethod
    def get_service_name(self) -> str:
        """Return the name of the service."""
        pass
    
    @abstractmethod
    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """Handle the initial message in the conversation flow."""
        pass
    
    @abstractmethod
    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle user response based on current conversation state.
        
        Args:
            message (Dict[str, Any]): The incoming message from the user
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        pass
    
    def create_text_message(self, body: str) -> Dict[str, Any]:
        """
        Create a text message payload.
        
        Args:
            body (str): Message text
            
        Returns:
            Dict[str, Any]: Message payload
        """
        return TextMessagePayload(
            to=self.recipient,
            body=body
        ).to_dict()
    
    def get_conversation_state(self) -> str:
        """Get current conversation state."""
        return self.conversation_state
    
    def set_conversation_state(self, state: str) -> None:
        """
        Set conversation state.
        
        Args:
            state (str): New state to set
        """
        self.conversation_state = state