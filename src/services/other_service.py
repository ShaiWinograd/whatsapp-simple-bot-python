"""Service for handling other/non-work related inquiries."""
from typing import List, Dict, Any

from src.services.base_service import BaseConversationService
from src.config.responses import SERVICE_RESPONSES
from webhook_payload import TextMessagePayload, InteractiveMessagePayload


class OtherService(BaseConversationService):
    """Service for handling other inquiries."""
    
    def get_service_name(self) -> str:
        """Return the name of the service."""
        return 'other'

    def __init__(self, recipient: str):
        """Initialize the other service."""
        super().__init__(recipient)
        self.responses = SERVICE_RESPONSES['אחר']
        self.state = 'initial'

    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """Handle the initial message for other inquiry."""
        self.state = 'initial'
        return [
            InteractiveMessagePayload(
                to=self.recipient,
                body=self.responses['initial']['welcome'],
                button_messages=self.responses['initial']['options']['buttons']
            ).to_dict()
        ]

    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle user responses in the other flow."""
        if self.state == 'initial':
            button_reply = (
                message.get('interactive', {}).get('button_reply', {}).get('title')
                or message.get('reply', {}).get('buttons_reply', {}).get('title', '')
            )
            
            if button_reply == 'לא':
                self.state = 'completed'
                return [
                    TextMessagePayload(
                        to=self.recipient,
                        body=self.responses['completed']['no_response']
                    ).to_dict()
                ]
            elif button_reply == 'כן':
                self.state = 'awaiting_service'
                return [
                    InteractiveMessagePayload(
                        to=self.recipient,
                        body=self.responses['awaiting_service']['question'],
                        button_messages=self.responses['awaiting_service']['options']['buttons']
                    ).to_dict()
                ]
        
        elif self.state == 'awaiting_service':
            button_reply = (
                message.get('interactive', {}).get('button_reply', {}).get('title')
                or message.get('reply', {}).get('buttons_reply', {}).get('title', '')
            )
            
            if button_reply == 'חזרה לתפריט הראשי':
                from src.message_handler import create_welcome_messages
                return create_welcome_messages(self.recipient)
            elif button_reply == 'הסבר על השירות הנדרש':
                self.state = 'awaiting_callback'
                return [
                    TextMessagePayload(
                        to=self.recipient,
                        body="אנא הסבר/י במה אני יכולה לעזור:"
                    ).to_dict()
                ]
        
        elif self.state == 'awaiting_callback':
            # Any text message here should trigger the callback scheduling
            if message.get('type') == 'text':
                self.state = 'completed'
                return [
                    TextMessagePayload(
                        to=self.recipient,
                        body=self.responses['completed']['schedule_callback']
                    ).to_dict()
                ]

        return super().handle_response(message)