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
        self.responses = SERVICE_RESPONSES['moving']

    def get_service_name(self) -> str:
        return self.responses['service_name']

    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """
        Handle initial moving service conversation.
        
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        self.set_conversation_state("awaiting_packing_choice")
        print("\nCreating initial moving service message...")
        initial_response = self.responses['initial']
        
        # Create list of button data
        buttons = [
            {"id": str(idx), "title": button}
            for idx, button in enumerate(initial_response['options']['buttons'])
        ]
        print(f"Created button data: {buttons}")

        payload = create_interactive_message(
            recipient=self.recipient,
            body_text=initial_response['welcome'],
            header_text=initial_response['header'],
            footer_text=initial_response['footer'],
            buttons=buttons
        )
        print(f"Created initial moving service payload: {payload}")

        return [payload]

    def _create_photo_requirement_message(self) -> List[Dict[str, Any]]:
        """Create photo requirement messages with options."""
        photo_msg = self.create_text_message(self.responses['photo_requirement']['message'])
        photo_options = create_interactive_message(
            recipient=self.recipient,
            body_text=self.responses['photo_requirement']['options']['title'],
            header_text=self.responses['photos']['header'],
            footer_text=self.responses['photos']['footer'],
            buttons=[{"id": str(i), "title": btn} for i, btn in enumerate(self.responses['photo_requirement']['options']['buttons'])]
        )
        return [photo_msg, photo_options]

    def _create_quote_message(self) -> Dict[str, Any]:
        """Create quote message based on service type."""
        quote_type = self.service_type
        quote_config = self.responses['price_quote'][quote_type if quote_type == 'both' else f"{quote_type}_only"]
        
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
            verify_options = create_interactive_message(
                recipient=self.recipient,
                body_text=self.responses['verify_details']['message'].format(details=self.customer_details),
                header_text=self.responses['verify']['header'],
                footer_text=self.responses['verify']['footer'],
                buttons=[{"id": str(i), "title": btn} for i, btn in enumerate(self.responses['verify_details']['options']['buttons'])]
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
        if button_title == NAVIGATION['back_to_main']:
            return self.handle_initial_message()
        elif button_title == NAVIGATION['talk_to_representative']:
            return []  # Will be handled by parent service
        
        # Check message type directly from root
        message_type = message.get('type', '')
        
        if message_type in ['image', 'video']:
            print("DEBUG - Image received, creating completion messages")
            self.set_conversation_state("completed")
            # Create scheduling message with available slots
            completion_messages = self._create_completion_messages()
            if not completion_messages:  # If completion messages failed
                print("ERROR - Failed to create completion messages")
                return [self.create_text_message(GENERAL['error'])]
            return completion_messages
            
        # If not an image/video, remind about photos and show navigation options
        return [
            self.create_text_message(self.responses['photo_requirement']['message']),
            create_interactive_message(
                recipient=self.recipient,
                body_text=self.responses['photo_requirement']['options']['title'],
                header_text=self.responses['photos']['header'],
                footer_text=self.responses['photos']['footer'],
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
            "awaiting_photos": self._handle_photos,
            "completed": lambda _: []  # Return empty list when completed to avoid further messages
        }
        
        current_state = self.get_conversation_state()
        handler = state_handlers.get(current_state)
        
        if handler:
            return handler(message)
        return [self.create_text_message(GENERAL['error'])]

    def _create_completion_messages(self) -> List[Dict[str, Any]]:
        """Helper method to create completion messages."""
        print("DEBUG - Starting to create completion messages")
        messages = []
        
        try:
            # Update labels silently
            print("DEBUG - Updating labels")
            WhatsAppClient.remove_label(self.recipient, LABELS['bot_new_conversation'])
            WhatsAppClient.apply_label(self.recipient, LABELS['waiting_quote'])
            
            # Create final message explaining the phone call requirement
            print("DEBUG - Getting completion message from responses")
            print(f"DEBUG - Available response keys: {list(self.responses.keys())}")
            completion_message = self.responses['completed']['after_media']
            if not completion_message:
                raise ValueError("Completion message is empty")
            print(f"DEBUG - Got completion message: {completion_message[:50]}...")

            # Get dynamic slots
            print("DEBUG - Getting available slots")
            available_slots = get_available_slots()
            if not available_slots:
                raise ValueError("No available slots returned")
            print(f"DEBUG - Got {len(available_slots)} available slots")

            # Add navigation options to the slots
            print("DEBUG - Adding navigation options to slots")
            available_slots.extend([
                {"id": "main_menu", "title": NAVIGATION['back_to_main']},
                {"id": "support", "title": NAVIGATION['talk_to_representative']}
            ])
            print(f"DEBUG - Total buttons after adding navigation: {len(available_slots)}")

            # Create scheduling message
            print("DEBUG - Creating interactive message")
            schedule_msg = create_interactive_message(
                recipient=self.recipient,
                body_text=completion_message,
                header_text=self.responses['scheduling']['header'],
                footer_text=self.responses['scheduling']['footer'],
                buttons=available_slots
            )
            if not schedule_msg:
                raise ValueError("Failed to create interactive message")
            messages.append(schedule_msg)
            
            print("DEBUG - Successfully created completion messages")
            return messages
        except Exception as e:
            print(f"ERROR in _create_completion_messages: {e}")
            # Create a simpler fallback message without slots
            fallback_msg = create_interactive_message(
                recipient=self.recipient,
                body_text=self.responses['fallback']['body'],
                header_text=self.responses['fallback']['header'],
                footer_text=self.responses['fallback']['footer'],
                buttons=[
                    {"id": "0", "title": NAVIGATION['back_to_main']},
                    {"id": "1", "title": NAVIGATION['talk_to_representative']}
                ]
            )
            return [fallback_msg]
        