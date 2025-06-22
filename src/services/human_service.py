"""Service for handling human support requests."""
from typing import List, Dict, Any

from .base_service import BaseConversationService
from ..config.responses import SERVICE_RESPONSES
from ..config.whatsapp import LABELS as WHATSAPP_LABELS
from ..models.webhook_payload import TextMessagePayload, InteractiveMessagePayload
from ..utils.whatsapp_client import WhatsAppClient


class HumanSupportService(BaseConversationService):
    """Service for handling human support requests."""
    
    def get_service_name(self) -> str:
        """Return the name of the service."""
        return 'human_support'

    def __init__(self, recipient: str):
        """Initialize the human support service."""
        super().__init__(recipient)
        self.responses = SERVICE_RESPONSES['human_support']
        self.state = 'initial'

    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """Handle the initial message for human support request."""
        self.state = 'completed'  # Immediately complete since we're transferring to human
        
        # Update labels: remove bot conversation label and add waiting human support label
        if WHATSAPP_LABELS['waiting_human_support']:
            WhatsAppClient.apply_label(
                self.recipient,
                WHATSAPP_LABELS['waiting_human_support']
            )
            
        if WHATSAPP_LABELS['bot_new_conversation']:
            WhatsAppClient.remove_label(
                self.recipient,
                WHATSAPP_LABELS['bot_new_conversation']
            )
        
        return [
            TextMessagePayload(
                to=self.recipient,
                body=self.responses['transfer_message']
            ).to_dict()
        ]

    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle user responses in the human support flow."""
        # For human support, we don't handle further responses
        # as the conversation is transferred to a human agent
        return []