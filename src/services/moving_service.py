"""Service for handling moving home conversation flow."""
from typing import List, Dict, Any
from .base_service import BaseConversationService
from ..config.responses.moving import (
    RESPONSES as MOVING_RESPONSES,
    SERVICE,
    URGENT_SUPPORT_MESSAGE,
    TIME_SLOTS,
    SELECTED_SLOT,
    EMERGENCY_SUPPORT,
    INITIAL,
    DETAILS_COLLECTION,
    VERIFY_DETAILS,
    VERIFY,
    PHOTOS
)
from ..config.responses.common import NAVIGATION, GENERAL
from ..utils.interactive_message_utils import get_button_title
from ..models.webhook_payload import TextMessagePayload



class MovingService(BaseConversationService):
    """Service for handling moving home related conversations with state management."""
    
    def __init__(self, recipient: str, conversation_manager=None):
        """
        Initialize the MovingService.
        
        Args:
            recipient (str): The recipient's phone number
            conversation_manager: Optional conversation manager instance
        """
        self.service_type: str | None = None
        self.selected_time_slot: str | None = None
        self.responses = MOVING_RESPONSES
        super().__init__(recipient, conversation_manager)

    def get_service_name(self) -> str:
        """Return the name of the service."""
        return SERVICE['name']


    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """Handle initial moving service conversation."""
        self.set_conversation_state("awaiting_packing_choice")
        print("\nCreating initial moving service message...")
        return [self._create_interactive_message_from_config(INITIAL)]

    def _reset_to_main_menu(self) -> List[Dict[str, Any]]:
        """Reset service state and return to main menu."""
        # Reset service data
        self.service_type = None
        self.selected_time_slot = None
        self.customer_details = None
        self.set_conversation_state("initial")
        
        # Return welcome message using common configuration
        return [self._create_interactive_message_from_config({
            'body': f"{GENERAL['intro']}\n\n{GENERAL['welcome_message']}",
            'header': GENERAL['header'],
            'footer': GENERAL['footer'],
            'buttons': GENERAL['options']
        })]

    def _handle_packing_choice(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle the packing choice state."""
        selected_option = get_button_title(message)
        
        if selected_option == NAVIGATION['back_to_main']:
            return self._reset_to_main_menu()
        elif selected_option == NAVIGATION['talk_to_representative']:
            self.set_conversation_state("awaiting_emergency_support")
            return [self._create_emergency_support_message()]
        
        option_map = {
            "אריזת הבית": "packing",
            "סידור בבית החדש": "unpacking",
            "ליווי מלא - אריזה וסידור": "both"
        }
        
        if selected_option in option_map:
            self.service_type = option_map[selected_option]
            self.set_conversation_state("awaiting_customer_details")
            return [self._create_details_message()]
            
        return [self.create_text_message(GENERAL['error'])]

    def _create_details_message(self) -> Dict[str, Any]:
        """Create message for collecting customer details based on service type."""
        service_type_map = {
            "packing": "packing_only",
            "unpacking": "unpacking_only",
            "both": "both"
        }
        
        if not self.service_type or self.service_type not in service_type_map:
            return self.create_text_message(GENERAL['error'])
            
        try:
            config = DETAILS_COLLECTION[service_type_map[self.service_type]]
            return self._create_interactive_message_from_config(config)
        except KeyError:
            print("Missing required config keys for details message")
            return self.create_text_message(GENERAL['error'])

    def _create_emergency_support_message(self) -> Dict[str, Any]:
        """Create emergency support confirmation message."""
        return self._create_interactive_message_from_config(EMERGENCY_SUPPORT)

    def _handle_emergency_support(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle response to emergency support question."""
        selected_option = get_button_title(message)
        if selected_option == 'כן':
            self.set_conversation_state("awaiting_emergency_support")
            # Create text message with proper type field to avoid handler recursion
            return [self.create_text_message(URGENT_SUPPORT_MESSAGE)]
        elif selected_option == 'לא':
            self.set_conversation_state("awaiting_slot_selection")
            return [self._create_interactive_message_from_config(TIME_SLOTS)]
        return [self.create_text_message(GENERAL['error'])]

    def _handle_slot_selection(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle time slot selection response."""
        selected_option = get_button_title(message)
        
        if selected_option == NAVIGATION['back_to_main']:
            return self._reset_to_main_menu()
        elif selected_option == NAVIGATION['talk_to_representative']:
            if self.conversation_manager:
                self.conversation_manager.update_service_state(self.recipient, "awaiting_emergency_support")
            else:
                self.set_conversation_state("awaiting_emergency_support")
            return [self._create_emergency_support_message()]
        elif selected_option == 'לקבוע זמן אחר':
            return [self._create_interactive_message_from_config(TIME_SLOTS)]
            
        if selected_option in TIME_SLOTS['buttons']:
            self.selected_time_slot = selected_option
            if self.conversation_manager:
                self.conversation_manager.update_service_state(self.recipient, "completed")
            else:
                self.set_conversation_state("completed")
            config = SELECTED_SLOT.copy()
            config['body'] = config['body'].format(slot=self.selected_time_slot)
            return [self._create_interactive_message_from_config(config)]
            
        return [self.create_text_message(GENERAL['error'])]

    def _handle_photos(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle photo submission or skip option."""
        if 'image' in message:
            self.set_conversation_state("awaiting_slot_selection")
            return [self._create_interactive_message_from_config(TIME_SLOTS)]
        selected_option = get_button_title(message)
        if selected_option == 'מעדיפים לדלג':
            self.set_conversation_state("awaiting_slot_selection")
            return [self._create_interactive_message_from_config(TIME_SLOTS)]
        return [self.create_text_message(GENERAL['error'])]

    def _handle_customer_details(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle customer details submission."""
        if not message or 'text' not in message:
            return [self.create_text_message(GENERAL['error'])]
            
        text = message.get('text', {}).get('body', '').strip()
        if not text:
            return [self._create_details_message()]
            
        self.customer_details = text
        
        self.set_conversation_state("awaiting_verification")
            
        verify_config = {
            'body': VERIFY_DETAILS['message'].format(details=self.customer_details),
            'header': VERIFY['header'],
            'footer': VERIFY['footer'],
            'buttons': VERIFY_DETAILS['options']['buttons']
        }
        return [self._create_interactive_message_from_config(verify_config)]
        
    def _handle_verification(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle verification of customer details."""
        selected_option = get_button_title(message)
        
        if selected_option == 'כן':
            self.set_conversation_state("awaiting_photos")
            return [self._create_interactive_message_from_config(PHOTOS)]
        elif selected_option == 'לא':
            self.set_conversation_state("awaiting_customer_details")
            return [self._create_details_message()]
            
        return [self.create_text_message(GENERAL['error'])]

    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle user response based on current conversation state."""
        if get_button_title(message) == NAVIGATION['back_to_main']:
            return self._reset_to_main_menu()
            
        valid_states = {
            "awaiting_packing_choice": self._handle_packing_choice,
            "awaiting_customer_details": self._handle_customer_details,
            "awaiting_verification": self._handle_verification,
            "awaiting_photos": self._handle_photos,
            "awaiting_emergency_support": self._handle_emergency_support,
            "awaiting_slot_selection": self._handle_slot_selection,
            "completed": lambda _: []
        }
        
        current_state = self.get_conversation_state()
        
        if current_state not in valid_states:
            print(f"Invalid state encountered: {current_state}")
            self.set_conversation_state("awaiting_packing_choice")
            return self.handle_initial_message()
            
        try:
            handler = valid_states[current_state]
            return handler(message)
        except Exception as e:
            print(f"Error handling response in state {current_state}: {str(e)}")
            return [self.create_text_message(GENERAL['error'])]
