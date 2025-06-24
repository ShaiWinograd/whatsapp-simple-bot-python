"""Service for handling moving home conversation flow."""
from typing import List, Dict, Any
from .base_service import BaseConversationService
from ..config.responses import SERVICE_RESPONSES
from ..config.responses.common import NAVIGATION, GENERAL
from ..utils.interactive_message_utils import get_button_title


class MovingService(BaseConversationService):
    """Service for handling moving home related conversations with state management."""

    def __init__(self, recipient: str):
        """
        Initialize the MovingService.
        
        Args:
            recipient (str): The recipient's phone number
        """
        super().__init__(recipient)
        self.service_type: str | None = None
        self.responses = SERVICE_RESPONSES['moving']

    def get_service_name(self) -> str:
        return self.responses['service_name']


    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """Handle initial moving service conversation."""
        try:
            self.set_conversation_state("awaiting_packing_choice")
            print("\nCreating initial moving service message...")
            
            if 'initial' not in self.responses:
                raise KeyError("Missing 'initial' configuration in responses")
                
            config = self.responses['initial']
            if not config.get('body'):
                raise KeyError("Missing 'body' field in initial configuration")
                
            payload = self._create_interactive_message_from_config(config)
            print(f"Created initial moving service payload: {payload}")
            return [payload]
            
        except Exception as e:
            print(f"Error creating initial moving service message: {str(e)}")
            return [self.create_text_message(GENERAL['error'])]

    def _create_photo_requirement_message(self) -> List[Dict[str, Any]]:
        """Create photo requirement messages with options."""
        photo_msg = self.create_text_message(self.responses['photo_requirement']['message'])
        photo_options = self._create_interactive_message_with_options({
            'header': self.responses['photos']['header'],
            'footer': self.responses['photos']['footer'],
            'options': self.responses['photo_requirement']['options']
        })
        return [photo_msg, photo_options]

    def _get_address_type_for_service(self) -> str:
        """Get the appropriate address type text based on service type."""
        if self.service_type == "packing":
            return 'כתובת נוכחית (כולל עיר, רחוב ומספר בית)'
        elif self.service_type == "unpacking":
            return 'כתובת חדשה (כולל עיר, רחוב ומספר בית)'
        else:  # both
            return 'כתובת נוכחית וחדשה (כולל עיר, רחוב ומספר בית)'

    def _create_details_message(self) -> Dict[str, Any]:
        """Create details collection message based on service type."""
        details_type = self.service_type if self.service_type == 'both' else f"{self.service_type}_only"
        details_config = self.responses['details_collection'][details_type]
        return self._create_interactive_message_from_config(details_config)

    def _create_rewrite_details_message(self) -> Dict[str, Any]:
        """Create rewrite details message with proper address type."""
        rewrite_config = self.responses['rewrite_details']
        address_type = self._get_address_type_for_service()
        
        config = {
            'body': rewrite_config['body'].format(address_type=address_type),
            'header': rewrite_config['header'],
            'footer': rewrite_config['footer'],
            'buttons': rewrite_config['buttons']
        }
        return self._create_interactive_message_from_config(config)

    def _handle_packing_choice(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle the packing choice state of the conversation.
        
        Args:
            message (Dict[str, Any]): The incoming message from the user
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        selected_option = get_button_title(message)
        option_map = {
            "אריזת הבית": "packing",
            "סידור בבית החדש": "unpacking",
            "ליווי מלא - אריזה וסידור": "both",
            NAVIGATION['back_to_main']: "back",
            NAVIGATION['talk_to_representative']: "support"
        }

        if selected_option == NAVIGATION['back_to_main']:
            return self.handle_initial_message()
        elif selected_option == NAVIGATION['talk_to_representative']:
            return []
        elif selected_option in option_map:
            self.service_type = option_map[selected_option]
            details_msg = self._create_details_message()
            self.set_conversation_state("awaiting_customer_details")
            return [details_msg]
        return [self.create_text_message(GENERAL['error'])]

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
            
        if len(text) < 20:  # Basic validation for minimum detail length
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
            self.set_conversation_state("awaiting_photos")
            return self._create_photo_requirement_message()
        elif button_title == 'לא, צריך לתקן':
            # Reset details but keep the service type
            self.customer_details = None
            # Set state back to awaiting details
            self.set_conversation_state("awaiting_customer_details")
            # Send the rewrite details message with proper address type
            return [self._create_rewrite_details_message()]
        return [self.create_text_message(GENERAL['error'])]

    def _handle_photos(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle the photo collection state of the conversation.
        
        Args:
            message (Dict[str, Any]): The incoming message containing photo, video, or button press
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
            
        Note:
            Accepts images, videos, or allows skipping the photo requirement.
            Returns to photo requirement options if invalid input is received.
        """
        try:
            # Handle navigation buttons first
            button_title = get_button_title(message)
            button_actions = {
                NAVIGATION['back_to_main']: self.handle_initial_message,
                NAVIGATION['talk_to_representative']: lambda: [],
                'מעדיפים לדלג': self._create_completion_messages
            }
            
            if button_title in button_actions:
                return button_actions[button_title]()
            
            # Check message type directly from root
            message_type = message.get('type', '')
            valid_media_types = ['image', 'video']
            
            if message_type in valid_media_types:
                # Could add media validation here if needed
                media_id = message.get(message_type, {}).get('id')
                if not media_id:
                    raise ValueError(f"Invalid {message_type} message: missing media ID")
                return self._create_completion_messages()
                
            # If not a valid submission, get photo requirement config
            photo_config = self.responses.get('photo_requirement', {})
            photos_config = self.responses.get('photos', {})
            options_config = photo_config.get('options', {})
            
            if not all([photo_config, photos_config, options_config]):
                raise ValueError("Missing required photo configuration")
                
            # Create reminder messages
            return [
                self.create_text_message(photo_config['message']),
                self._create_interactive_message_with_options({
                    'header': photos_config.get('header', ''),
                    'footer': photos_config.get('footer', ''),
                    'options': options_config
                })
            ]
            
        except Exception as e:
            print(f"Error handling photos: {str(e)}")
            return [self.create_text_message(GENERAL['error'])]


    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle user response based on current conversation state.
        
        Args:
            message (Dict[str, Any]): The incoming message from the user
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
            
        Note:
            Validates current state and ensures proper state transitions.
            Falls back to initial state if invalid state is encountered.
        """
        valid_states = {
            "awaiting_packing_choice": self._handle_packing_choice,
            "awaiting_customer_details": self._handle_customer_details,
            "awaiting_verification": self._handle_verification,
            "awaiting_photos": self._handle_photos,
            "awaiting_slot_selection": self._handle_slot_selection,
            "completed": lambda _: []  # Return empty list when completed
        }
        
        current_state = self.get_conversation_state()
        
        # Validate current state
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
