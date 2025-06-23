"""Service for handling moving home conversation flow."""
from typing import List, Dict, Any
from .base_service import BaseConversationService
from ..config.responses import SERVICE_RESPONSES, GENERAL
from ..config.responses.common import NAVIGATION
from ..config.whatsapp import LABELS
from ..utils.interactive_message_utils import get_button_title
from ..utils.interactive_message_builder import create_interactive_message
from ..utils.scheduling import get_available_slots
from ..utils.whatsapp_client import WhatsAppClient


class MovingService(BaseConversationService):
    """Service for handling moving home related conversations."""

    def __init__(self, recipient: str):
        super().__init__(recipient)
        self.service_type = None
        self.customer_details = None

    def get_service_name(self) -> str:
        return "מעבר דירה"

    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """
        Handle initial moving service conversation.
        
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        self.set_conversation_state("awaiting_packing_choice")
        print("\nCreating initial moving service message...")
        responses = SERVICE_RESPONSES['moving']['initial']
        
        # Create list of button data
        buttons = [
            {"id": str(idx), "title": button}
            for idx, button in enumerate(responses['options']['buttons'])
        ]
        print(f"Created button data: {buttons}")

        payload = create_interactive_message(
            recipient=self.recipient,
            body_text=responses['welcome'],
            header_text=responses['header'],
            footer_text=responses['footer'],
            buttons=buttons
        )
        print(f"Created initial moving service payload: {payload}")

        return [payload]

    def _create_photo_requirement_message(self) -> List[Dict[str, Any]]:
        """Create photo requirement messages with options."""
        responses = SERVICE_RESPONSES['moving']
        photo_msg = self.create_text_message(responses['photo_requirement']['message'])
        photo_options = create_interactive_message(
            recipient=self.recipient,
            body_text=responses['photo_requirement']['options']['title'],
            header_text="שליחת תמונות 📸",
            footer_text="התמונות יעזרו לנו להעריך את היקף העבודה",
            buttons=[{"id": str(i), "title": btn} for i, btn in enumerate(responses['photo_requirement']['options']['buttons'])]
        )
        return [photo_msg, photo_options]

    def _create_quote_message(self) -> Dict[str, Any]:
        """Create quote message based on service type."""
        responses = SERVICE_RESPONSES['moving']
        quote_type = self.service_type
        quote_config = responses['price_quote'][quote_type if quote_type == 'both' else f"{quote_type}_only"]
        
        return create_interactive_message(
            recipient=self.recipient,
            body_text=quote_config['body'],
            header_text=quote_config['header'],
            footer_text=quote_config['footer'],
            buttons=[{"id": str(i), "title": btn} for i, btn in enumerate(quote_config['buttons'])]
        )

    def _handle_packing_choice(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle packing choice state."""
        selected_option = get_button_title(message)
        option_map = {
            "אריזה 📦": "packing",
            "סידור אחרי המעבר 🏡": "unpacking",
            "גם וגם ✨": "both"
        }

        if selected_option in option_map:
            self.service_type = option_map[selected_option]
            quote_msg = self._create_quote_message()
            self.set_conversation_state("awaiting_customer_details")
            return [quote_msg]
        return [self.create_text_message(GENERAL['error'])]

    def _handle_customer_details(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle customer details state."""
        text = message.get('text', {}).get('body', '')
        if text:
            # Save the details and create verification message
            self.customer_details = text
            responses = SERVICE_RESPONSES['moving']
            verify_options = create_interactive_message(
                recipient=self.recipient,
                body_text=responses['verify_details']['message'].format(details=self.customer_details),
                header_text="✅ אימות פרטים",
                footer_text="אנא אשר/י שהפרטים נכונים",
                buttons=[{"id": str(i), "title": btn} for i, btn in enumerate(responses['verify_details']['options']['buttons'])]
            )
            # Set state to awaiting verification
            self.set_conversation_state("awaiting_verification")
            return [verify_options]
        
        # If no text provided, send the quote message again
        return [self._create_quote_message()]

    def _handle_verification(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle verification state."""
        button_title = get_button_title(message)
        
        if button_title == 'כן, הפרטים נכונים ✅':
            self.set_conversation_state("awaiting_photos")
            return self._create_photo_requirement_message()
        elif button_title == 'לא, צריך לתקן ❌':
            # Reset details but keep the service type
            self.customer_details = None
            # Set state back to awaiting details
            self.set_conversation_state("awaiting_customer_details")
            # Send the quote message again
            return [self._create_quote_message()]
        return [self.create_text_message(GENERAL['error'])]

    def _handle_photos(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle photos state."""
        print(f"DEBUG - Handling photo message: {message}")
        
        # Handle navigation buttons first
        button_title = get_button_title(message)
        if button_title in [NAVIGATION['back_to_main'], NAVIGATION['talk_to_representative']]:
            return []

        responses = SERVICE_RESPONSES['moving']
        
        # Check message type directly from root
        message_type = message.get('type', '')
        
        if message_type in ['image', 'video']:
            self.set_conversation_state("completed")
            messages = [self.create_text_message(responses['completed']['after_media'])]
            messages.extend(self._create_completion_messages())
            return messages
            
        # If not an image/video, remind about photos and show navigation options
        return [
            self.create_text_message(responses['photo_requirement']['message']),
            create_interactive_message(
                recipient=self.recipient,
                body_text=responses['photo_requirement']['options']['title'],
                header_text="שליחת תמונות 📸",
                footer_text="התמונות יעזרו לנו להעריך את היקף העבודה",
                buttons=[
                    {"id": "main_menu", "title": NAVIGATION['back_to_main']},
                    {"id": "support", "title": NAVIGATION['talk_to_representative']}
                ]
            )
        ]

    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle user response based on current conversation state."""
        state_handlers = {
            "awaiting_packing_choice": self._handle_packing_choice,
            "awaiting_customer_details": self._handle_customer_details,
            "awaiting_verification": self._handle_verification,
            "awaiting_photos": self._handle_photos
        }
        
        current_state = self.get_conversation_state()
        handler = state_handlers.get(current_state)
        
        if handler:
            return handler(message)
        return [self.create_text_message(GENERAL['error'])]

    def _create_completion_messages(self, responses) -> List[Dict[str, Any]]:
        """Helper method to create completion messages."""
        messages = []
        
        # Update labels silently
        WhatsAppClient.remove_label(self.recipient, LABELS['bot_new_conversation'])
        WhatsAppClient.apply_label(self.recipient, LABELS['waiting_quote'])
        
        # Create final message explaining the phone call requirement
        completion_responses = responses['completion']['after_media']

        # Get dynamic slots
        available_slots = get_available_slots()
        
        # Add navigation options to the slots
        available_slots.extend([
            {"id": "main_menu", "title": NAVIGATION['back_to_main']},
            {"id": "support", "title": NAVIGATION['talk_to_representative']}
        ])
        
        # Create scheduling message
        schedule_msg = create_interactive_message(
            recipient=self.recipient,
            body_text=completion_responses,
            header_text="תיאום שיחת טלפון 📞",
            footer_text="",
            buttons=available_slots
        )
        messages.append(schedule_msg)
        
        return messages