"""Service for handling human support requests."""
from typing import List, Dict, Any

from .base_service import BaseConversationService
from ..config.responses import SERVICE_RESPONSES
from ..models.webhook_payload import TextMessagePayload, InteractiveMessagePayload


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