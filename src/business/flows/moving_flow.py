"""Moving service flow implementation."""
from typing import Dict, Any, Optional
import logging

from .abstract_business_flow import AbstractBusinessFlow
from ...whatsapp.utils.message_parser import get_button_title
from ...models.message_payload import MessagePayloadBuilder
from .moving.messages import (
    RESPONSES as MOVING_RESPONSES,
    TIME_SLOTS,
    SELECTED_SLOT,
    EMERGENCY_SUPPORT,
    DETAILS_COLLECTION,
    VERIFY_DETAILS,
    PHOTOS
)
from src.config.responses.common import NAVIGATION, GENERAL
from .moving.validator import MovingFlowValidator

logger = logging.getLogger(__name__)

class MovingFlow(AbstractBusinessFlow):
    """Handles the moving service business flow"""
    
    def __init__(self):
        super().__init__()
        self._states = {
            'initial': self._handle_initial_state,
            'awaiting_packing_choice': self._handle_packing_choice,
            'awaiting_customer_details': self._handle_customer_details,
            'awaiting_verification': self._handle_verification,
            'awaiting_photos': self._handle_photos,
            'awaiting_emergency_support': self._handle_emergency_support,
            'awaiting_slot_selection': self._handle_slot_selection,
            'awaiting_reschedule': self._handle_reschedule,
            'completed': self._handle_completed_state
        }
        self._service_type: Optional[str] = None
        self._selected_time_slot: Optional[str] = None
        self._customer_details: Optional[str] = None
        self._validator = MovingFlowValidator()

    def get_flow_name(self) -> str:
        """Get the name of this business flow"""
        return 'moving'

    def handle_input(self, user_input: str) -> str:
        """Handle user input based on current state"""
        try:
            # Global navigation commands take absolute precedence
            if user_input == NAVIGATION['back_to_main']:
                self.set_conversation_state('initial')
                return 'initial'
            
            if user_input == NAVIGATION['talk_to_representative']:
                self.set_conversation_state('awaiting_emergency_support')
                return 'awaiting_emergency_support'
                
            # Service type selection
            if user_input in ['אריזת הבית', 'סידור בבית החדש', 'ליווי מלא - אריזה וסידור']:
                service_types = {
                    'אריזת הבית': 'packing_only',
                    'סידור בבית החדש': 'unpacking_only',
                    'ליווי מלא - אריזה וסידור': 'both'
                }
                self._service_type = service_types[user_input]
                self.set_conversation_state('awaiting_packing_choice')
                return 'awaiting_packing_choice'
            
            # State-specific handling
            state_handler = self._states.get(self._conversation_state)
            if state_handler:
                next_state = state_handler(user_input)
                self.set_conversation_state(next_state)
                return next_state
            
            self.set_conversation_state('initial')
            return 'initial'
        except Exception as e:
            logger.error(f"Error handling input: {str(e)}")
            self.set_conversation_state('initial')
            return 'initial'

    def _handle_initial_state(self, user_input: str) -> str:
        """Handle initial state input"""
        # Initial state only handles invalid inputs now
        # Service type selection is handled in handle_input
        return 'initial'

    def _handle_packing_choice(self, user_input: str) -> str:
        """Handle packing service details collection"""
        if self._validator.validate_customer_details(user_input):
            self._customer_details = user_input
            return 'awaiting_verification'
        return 'awaiting_packing_choice'

    def _handle_customer_details(self, user_input: str) -> str:
        """Handle customer details verification"""
        if self._validator.validate_customer_details(user_input):
            self._customer_details = user_input
            return 'awaiting_verification'
        return 'awaiting_customer_details'

    def _handle_verification(self, user_input: str) -> str:
        """Handle details verification"""
        if user_input == 'כן, הפרטים נכונים':
            return 'awaiting_photos'
        elif user_input == 'לא, צריך לתקן':
            return 'awaiting_customer_details'
        return 'awaiting_verification'

    def _handle_photos(self, user_input: str) -> str:
        """Handle photo submission"""
        if isinstance(user_input, dict):  # Handle photo data
            if self._validator.validate_photo(user_input):
                return 'awaiting_slot_selection'
        elif user_input == 'דלג':
            return 'awaiting_slot_selection'
        return 'awaiting_photos'

    def _handle_emergency_support(self, user_input: str) -> str:
        """Handle emergency support request"""
        if user_input == 'כן':
            return 'completed'  # Will trigger urgent support label
        return 'awaiting_slot_selection'

    def _handle_slot_selection(self, user_input: str) -> str:
        """Handle time slot selection"""
        if user_input in TIME_SLOTS['buttons']:
            self._selected_time_slot = user_input
            return 'completed'
        return 'awaiting_slot_selection'

    def _handle_reschedule(self, user_input: str) -> str:
        """Handle reschedule request"""
        if user_input in TIME_SLOTS['buttons']:
            self._selected_time_slot = user_input
            return 'completed'
        return 'awaiting_reschedule'

    def _handle_completed_state(self, user_input: str) -> str:
        """Handle completed state"""
        if user_input == 'לקבוע זמן אחר':
            return 'awaiting_reschedule'
        return 'completed'

    def get_next_message(self) -> str:
        """Get next message based on current state"""
        try:
            if not self._recipient:
                logger.error("Recipient not set for message creation")
                return MessagePayloadBuilder.create_interactive_message(
                    recipient=self._recipient,
                    body_text=GENERAL['error']
                )

            def create_message_from_template(template, **kwargs):
                buttons = [{"id": btn, "title": btn} for btn in template.get('buttons', [])] if 'buttons' in template else None
                return MessagePayloadBuilder.create_interactive_message(
                    recipient=self._recipient,
                    body_text=template.get('body', ''),
                    header_text=template.get('header', ''),
                    footer_text=template.get('footer', ''),
                    buttons=buttons,
                    **kwargs
                )

            if self._conversation_state == 'initial':
                return create_message_from_template(MOVING_RESPONSES['initial'])
                
            elif self._conversation_state == 'awaiting_packing_choice':
                return create_message_from_template(DETAILS_COLLECTION[self._service_type])
                
            elif self._conversation_state == 'awaiting_customer_details':
                return create_message_from_template(VERIFY_DETAILS)
                
            elif self._conversation_state == 'awaiting_verification':
                return create_message_from_template(
                    VERIFY_DETAILS,
                    body_text=VERIFY_DETAILS['body'].format(details=self._customer_details)
                )
                
            elif self._conversation_state == 'awaiting_photos':
                return create_message_from_template(PHOTOS)
                
            elif self._conversation_state == 'awaiting_emergency_support':
                return create_message_from_template(EMERGENCY_SUPPORT)
                
            elif self._conversation_state == 'awaiting_slot_selection':
                return create_message_from_template(TIME_SLOTS)
                
            elif self._conversation_state == 'awaiting_reschedule':
                return create_message_from_template(TIME_SLOTS)
                
            elif self._conversation_state == 'completed':
                return create_message_from_template(
                    SELECTED_SLOT,
                    body_text=SELECTED_SLOT['body'].format(slot=self._selected_time_slot)
                )

            logger.error(f"Invalid state for message: {self._conversation_state}")
            error_template = {'body': GENERAL['error']}
            return create_message_from_template(error_template)

        except Exception as e:
            logger.error(f"Error getting next message: {str(e)}")
            error_template = {'body': GENERAL['error']}
            return create_message_from_template(error_template)