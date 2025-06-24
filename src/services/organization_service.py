"""Service for handling organization conversation flow."""
from typing import List, Dict, Any
from .base_service import BaseConversationService
from ..config.responses import SERVICE_RESPONSES, GENERAL
from ..config.responses.common import NAVIGATION
from ..utils.interactive_message_utils import get_button_title


class OrganizationService(BaseConversationService):
    """Service for handling organization related conversations with state management."""

    def __init__(self, recipient: str):
        """
        Initialize the OrganizationService.
        
        Args:
            recipient (str): The recipient's phone number
        """
        super().__init__(recipient)
        self.responses = SERVICE_RESPONSES['organization']

    def get_service_name(self) -> str:
        return self.responses['service_name']


    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """Handle initial organization service conversation."""
        self.set_conversation_state("awaiting_customer_details")
        print("\nCreating details collection message...")
        # Apply organization service label
        self._apply_service_label('organization')
        return [self._create_details_message()]

    def _create_details_message(self) -> Dict[str, Any]:
        """Create details collection message."""
        return self._create_interactive_message_from_config({
            'body': self.responses['rewrite_details']['body'],
            'header': self.responses['rewrite_details']['header'],
            'footer': self.responses['rewrite_details']['footer'],
            'buttons': self.responses['rewrite_details']['buttons']
        })

    def _handle_customer_details(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle the customer details collection state.
        
        Args:
            message (Dict[str, Any]): The incoming message containing customer details
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        text = message.get('text', {}).get('body', '').strip()
        
        # Validate customer details
        if not text:
            return [self._create_details_message()]
            
        if len(text) < 25:  # Basic validation for minimum detail length
            return [
                self.create_text_message("בבקשה שלחו בהודעה אחת את כל הפרטים הנדרשים. לפי בדיקה שעשינו הפרטים שהתקבלו לא מספיקים."),
                self._create_details_message()
            ]
            
        # Save the details and create verification message
        self.customer_details = text
        self.set_conversation_state("awaiting_verification")
        return [self._create_verification_message()]

    def _handle_verification(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle verification state."""
        button_title = get_button_title(message)
        
        if button_title == 'כן, הפרטים נכונים':
            return self._create_completion_messages()
        elif button_title == 'לא, צריך לתקן':
            # Reset details but keep the space type
            self.customer_details = None
            # Set state back to awaiting details
            self.set_conversation_state("awaiting_customer_details")
            # Send the rewrite details message
            return [self._create_details_message()]
        return [self.create_text_message(GENERAL['error'])]


    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle user response based on current conversation state.
        
        Args:
            message (Dict[str, Any]): The incoming message from the user
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        valid_states = {
            "awaiting_customer_details": self._handle_customer_details,
            "awaiting_verification": self._handle_verification,
            "awaiting_slot_selection": self._handle_slot_selection,
            "completed": lambda _: []  # Return empty list when completed
        }
        
        current_state = self.get_conversation_state()
        
        # Validate current state
        if current_state not in valid_states:
            print(f"Invalid state encountered: {current_state}")
            self.set_conversation_state("awaiting_customer_details")
            return self.handle_initial_message()
            
        try:
            handler = valid_states[current_state]
            return handler(message)
        except Exception as e:
            print(f"Error handling response in state {current_state}: {str(e)}")
            return [self.create_text_message(GENERAL['error'])]
