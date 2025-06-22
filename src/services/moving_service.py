"""Service for handling moving home conversation flow."""
from typing import List, Dict, Any
from .base_service import BaseConversationService
from ..config.responses import SERVICE_RESPONSES, GENERAL
from ..utils.interactive_message_utils import get_button_title
from ..utils.interactive_message_builder import create_interactive_message


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

    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle user response based on current conversation state."""
        print(f"\nDEBUG - Handling response in MovingService")
        current_state = self.get_conversation_state()
        print(f"DEBUG - Current state: {current_state}")
        responses = SERVICE_RESPONSES['moving']

        if current_state == "awaiting_packing_choice":

            print(f"DEBUG - Processing packing choice")
            # Get button selection
            selected_option = get_button_title(message)
            print(f"DEBUG - Selected option from button: {selected_option}")
            
            # Map button titles to service types
            option_map = {
                "אריזה 📦": "packing",
                "סידור אחרי המעבר 🏡": "unpacking",
                "גם וגם ✨": "both"
            }

            print(f"DEBUG - Available options: {list(option_map.keys())}")
            if selected_option in option_map:
                print(f"DEBUG - Match found for option: {selected_option}")
                self.service_type = option_map[selected_option]
                print(f"DEBUG - Setting service type to: {self.service_type}")
                
                # Get quote config based on service type
                quote_type = self.service_type
                quote_config = responses['price_quote'][quote_type if quote_type == 'both' else f"{quote_type}_only"]
                
                # Create interactive message with header and footer
                quote_msg = create_interactive_message(
                    recipient=self.recipient,
                    body_text=quote_config['body'],
                    header_text=quote_config['header'],
                    footer_text=quote_config['footer'],
                    buttons=[{"id": str(i), "title": btn} for i, btn in enumerate(quote_config['buttons'])]
                )
                
                self.set_conversation_state("awaiting_customer_details")
                return [quote_msg]

        elif current_state == "awaiting_customer_details":
            # Store the raw message text
            text = message.get('text', {}).get('body', '')
            if text:
                self.customer_details = text

                # Show the raw text for verification
                verify_msg = self.create_text_message(
                    responses['verify_details']['message'].format(details=self.customer_details)
                )
                
                # Create interactive message for verification
                verify_options = create_interactive_message(
                    recipient=self.recipient,
                    body_text=responses['verify_details']['options']['title'],
                    header_text="✅ אימות פרטים",
                    footer_text="אנא אשר/י שהפרטים נכונים",
                    buttons=[{"id": str(i), "title": btn} for i, btn in enumerate(responses['verify_details']['options']['buttons'])]
                )

                self.set_conversation_state("awaiting_verification")
                return [verify_msg, verify_options]

        elif current_state == "awaiting_verification":
            button_title = get_button_title(message)
            
            if button_title == 'כן, הפרטים נכונים':
                self.set_conversation_state("awaiting_photos")
                photo_msg = self.create_text_message(responses['photo_requirement']['message'])
                
                # Create interactive message for photo requirement
                photo_options = create_interactive_message(
                    recipient=self.recipient,
                    body_text=responses['photo_requirement']['options']['title'],
                    header_text="📸 שליחת תמונות",
                    footer_text="התמונות יעזרו לנו להעריך את היקף העבודה",
                    buttons=[{"id": str(i), "title": btn} for i, btn in enumerate(responses['photo_requirement']['options']['buttons'])]
                )
                return [photo_msg, photo_options]
            elif button_title == 'לא, צריך לתקן':
                self.set_conversation_state("awaiting_customer_details")
                # Reset details and show appropriate message based on service type
                self.customer_details = None
                
                # Get quote config based on service type
                quote_type = self.service_type
                quote_config = responses['price_quote'][quote_type if quote_type == 'both' else f"{quote_type}_only"]
                
                # Create interactive message with header and footer
                quote_msg = {
                    'type': 'interactive',
                    'interactive': {
                        'type': 'button',
                        'header': {
                            'type': 'text',
                            'text': quote_config['header']
                        },
                        'body': {
                            'text': quote_config['body']
                        },
                        'footer': {
                            'text': quote_config['footer']
                        },
                        'action': {
                            'buttons': [
                                {'type': 'reply', 'reply': {'id': 'main_menu', 'title': button}}
                                for button in quote_config['buttons']
                            ]
                        }
                    }
                }
                return [quote_msg]

        elif current_state == "awaiting_photos":
            # After receiving photos, proceed to move type question
            self.set_conversation_state("awaiting_move_type")
            move_responses = responses['awaiting_move_type']

            # Create interactive message for move type
            location_msg = self.create_text_message(move_responses['question'])
            location_options = create_interactive_message(
                recipient=self.recipient,
                body_text=move_responses['options']['title'],
                header_text="🌍 סוג המעבר",
                footer_text="בחר/י את סוג המעבר המתאים",
                buttons=[{"id": str(i), "title": btn} for i, btn in enumerate(move_responses['options']['buttons'])]
            )

            return [location_msg, location_options]

        elif current_state == "awaiting_move_type":
            button_title = get_button_title(message)

            if button_title in responses['awaiting_move_type']['options']['buttons']:
                self.set_conversation_state("awaiting_property_size")
                size_msg = self.create_text_message(
                    responses['awaiting_property_size']['question']
                )
                return [size_msg]

        elif current_state == "awaiting_property_size":
            self.set_conversation_state("awaiting_move_date")
            date_msg = self.create_text_message(
                responses['awaiting_move_date']['question']
            )
            return [date_msg]

        elif current_state == "awaiting_move_date":
            self.set_conversation_state("completed")
            completion_responses = responses['completed']

            final_msg = self.create_text_message(completion_responses['final'])
            
            # Create interactive message for scheduling
            schedule_msg = create_interactive_message(
                recipient=self.recipient,
                body_text=completion_responses['schedule']['title'],
                header_text="📅 תיאום פגישה",
                footer_text="נשמח לקבוע זמן שנוח לך!",
                buttons=[{"id": str(i), "title": btn} for i, btn in enumerate(completion_responses['schedule']['buttons'])]
            )

            return [final_msg, schedule_msg]
        
        # Default response if state is unknown
        return [self.create_text_message(GENERAL['error'])]