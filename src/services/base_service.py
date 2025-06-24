"""Base service class for handling conversation flows."""
from abc import ABC, abstractmethod
from typing import List, Dict, Any
from ..utils.whatsapp_client import WhatsAppClient
from ..models.webhook_payload import TextMessagePayload
from ..config.responses.common import NAVIGATION, CALL_SCHEDULING, GENERAL
from ..utils.interactive_message_builder import create_interactive_message
from ..utils.interactive_message_utils import get_button_title
from ..utils.scheduling import get_available_slots


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
        self.customer_details: str | None = None
        self.responses: Dict[str, Any] = {}
        self.current_label = None
    
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

    def _create_interactive_message_from_config(self, config: Dict[str, Any], buttons_key: str = 'buttons') -> Dict[str, Any]:
        """
        Create an interactive message from configuration dictionary.
        
        Args:
            config (Dict[str, Any]): Configuration dictionary containing message details
            buttons_key (str, optional): Key for buttons in config. Defaults to 'buttons'
            
        Returns:
            Dict[str, Any]: WhatsApp API compatible interactive message payload
        """
        if not config.get('body'):
            raise KeyError("Required 'body' key missing from config")
            
        return create_interactive_message(
            recipient=self.recipient,
            body_text=config['body'],
            header_text=config.get('header', ''),
            footer_text=config.get('footer', ''),
            buttons=config.get(buttons_key, []) if all(isinstance(b, dict) and 'id' in b and 'title' in b for b in config.get(buttons_key, []))
                   else [{"id": str(i), "title": btn} for i, btn in enumerate(config.get(buttons_key, []))]
        )

    def _create_interactive_message_with_options(self, config: Dict[str, Any]) -> Dict[str, Any]:
        """Helper method to create interactive messages with options structure."""
        return create_interactive_message(
            recipient=self.recipient,
            body_text=config['options']['title'],
            header_text=config.get('header', ''),
            footer_text=config.get('footer', ''),
            buttons=config['options']['buttons'] if all(isinstance(b, dict) and 'id' in b and 'title' in b for b in config['options']['buttons'])
                   else [{"id": str(i), "title": btn} for i, btn in enumerate(config['options']['buttons'])]
        )

    def _create_verification_message(self) -> Dict[str, Any]:
        """
        Create a verification message with customer details.
        
        Returns:
            Dict[str, Any]: WhatsApp API compatible interactive message payload
        """
        if not self.customer_details:
            raise ValueError("Customer details must be set before creating verification message")
            
        try:
            verify_details = self.responses.get('verify_details', {})
            verify_config = self.responses.get('verify', {})
            
            if not verify_details or not verify_config:
                raise ValueError("Verification configuration is missing")
                
            return create_interactive_message(
                recipient=self.recipient,
                body_text=verify_details['message'].format(details=self.customer_details),
                header_text=verify_config.get('header', ''),
                footer_text=verify_config.get('footer', ''),
                buttons=[
                    {"id": str(i), "title": btn}
                    for i, btn in enumerate(verify_details.get('options', {}).get('buttons', []))
                ]
            )
        except Exception as e:
            print(f"Error creating verification message: {str(e)}")
            raise

    def _handle_slot_selection(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle the time slot selection state.
        
        Args:
            message (Dict[str, Any]): The incoming message containing selected slot
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        selected_slot = get_button_title(message)
        
        # Create response map for better maintainability
        response_map = {
            NAVIGATION['back_to_main']: lambda: self.handle_initial_message(),
            NAVIGATION['talk_to_representative']: lambda: [],
            'שינוי מועד השיחה': lambda: self._create_completion_messages()
        }
        
        # Handle predefined responses
        if selected_slot in response_map:
            return response_map[selected_slot]()
            
        # Validate selected slot format (basic check)
        if not selected_slot or len(selected_slot) < 5:  # Assuming minimum time slot format
            return [self.create_text_message(GENERAL['error'])]
            
        try:
            # Create confirmation message with option to change slot
            return [self._create_interactive_message_from_config({
                'body': CALL_SCHEDULING['confirmation']['body_template'].format(slot=selected_slot),
                'header': CALL_SCHEDULING['confirmation']['header'],
                'footer': CALL_SCHEDULING['confirmation']['footer'],
                'buttons': [CALL_SCHEDULING['confirmation']['change_slot_button']]
            })]
        except Exception as e:
            print(f"Error creating slot confirmation message: {str(e)}")
            return [self.create_text_message(GENERAL['error'])]

    def _apply_service_label(self, label_key: str) -> None:
        """
        Apply a service-specific label and remove previous one if exists.
        
        Args:
            label_key (str): Key for the label in LABELS config
        """
        from ..config.whatsapp import LABELS
        if self.current_label and self.current_label in LABELS:
            WhatsAppClient.remove_label(self.recipient, LABELS[self.current_label])
        if label_key in LABELS:
            WhatsAppClient.apply_label(self.recipient, LABELS[label_key])
            self.current_label = label_key

    def _remove_label(self, label_key: str) -> None:
        """
        Remove a service-specific label.
        
        Args:
            label_key (str): Key for the label in LABELS config
        """
        from ..config.whatsapp import LABELS
        if label_key in LABELS:
            WhatsAppClient.remove_label(self.recipient, LABELS[label_key])
            if self.current_label == label_key:
                self.current_label = None

    def _create_completion_messages(self) -> List[Dict[str, Any]]:
        """
        Create completion messages with available time slots.
        
        Returns:
            List[Dict[str, Any]]: List of completion messages
        """
        # Apply waiting for call label
        self._apply_service_label('waiting_call_before_quote')
        messages = []
        
        try:
            # Validate and get completion message
            completion_message = self.responses.get('completed', {}).get('after_media')
            if not completion_message:
                raise ValueError("Required completion message not found in responses")

            # Get and validate available slots
            available_slots = get_available_slots()
            if not available_slots:
                raise ValueError("No available time slots found")

            # Add navigation options to slots
            navigation_options = [
                {"id": "main_menu", "title": NAVIGATION['back_to_main']},
                {"id": "support", "title": NAVIGATION['talk_to_representative']}
            ]
            available_slots.extend(navigation_options)

            # Create and validate scheduling message
            schedule_msg = self._create_interactive_message_from_config({
                'body': completion_message,
                'header': self.responses.get('scheduling', {}).get('header', ''),
                'footer': self.responses.get('scheduling', {}).get('footer', ''),
                'buttons': available_slots
            })
            if not schedule_msg:
                raise ValueError("Failed to create interactive scheduling message")

            messages.append(schedule_msg)
            self.set_conversation_state("awaiting_slot_selection")
            
            return messages
            
        except Exception as e:
            print(f"Error creating completion messages: {str(e)}")
            # Create a simpler fallback message without slots
            return [self._create_interactive_message_from_config({
                'body': self.responses.get('fallback', {}).get('body', GENERAL['error']),
                'header': self.responses.get('fallback', {}).get('header', ''),
                'footer': self.responses.get('fallback', {}).get('footer', ''),
                'buttons': [
                    NAVIGATION['back_to_main'],
                    NAVIGATION['talk_to_representative']
                ]
            })]