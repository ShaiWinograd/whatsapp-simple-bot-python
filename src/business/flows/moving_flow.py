from typing import Dict, Any, Optional
import logging

from .abstract_business_flow import AbstractBusinessFlow
from ...whatsapp.utils.message_parser import get_button_title
from ...models.message_payload import MessagePayloadBuilder
from .moving.messages import (
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
from ..messages import NAVIGATION
from ...whatsapp.templates import GENERAL
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
            # Check for global navigation commands
            if user_input == NAVIGATION['back_to_main']:
                logger.info("User requested return to main menu")
                return 'initial'
            
            if user_input == NAVIGATION['talk_to_representative']:
                logger.info("User requested support")
                return 'awaiting_emergency_support'

            # Get appropriate state handler
            state_handler = self._states.get(self._conversation_state)
            if not state_handler:
                logger.error(f"Invalid state: {self._conversation_state}")
                return 'initial'

            # Handle state-specific input
            return state_handler(user_input)

        except Exception as e:
            logger.error(f"Error handling input: {str(e)}")
            return 'initial'

    def get_next_message(self) -> str:
        """Get next message based on current state"""
        try:
            if self._conversation_state == 'initial':
                return MessagePayloadBuilder.create_interactive_message(
                    MOVING_RESPONSES['initial']
                )
                
            elif self._conversation_state == 'awaiting_packing_choice':
                return MessagePayloadBuilder.create_interactive_message(
                    DETAILS_COLLECTION[self._service_type]
                )
                
            elif self._conversation_state == 'awaiting_customer_details':
                return MessagePayloadBuilder.create_interactive_message(
                    VERIFY_DETAILS
                )
                
            elif self._conversation_state == 'awaiting_verification':
                return MessagePayloadBuilder.create_interactive_message(
                    body_text=VERIFY_DETAILS['body'].format(details=self._customer_details)
                )
                
            elif self._conversation_state == 'awaiting_photos':
                return MessagePayloadBuilder.create_interactive_message(PHOTOS)
                
            elif self._conversation_state == 'awaiting_emergency_support':
                return MessagePayloadBuilder.create_interactive_message(EMERGENCY_SUPPORT)
                
            elif self._conversation_state == 'awaiting_slot_selection':
                return MessagePayloadBuilder.create_interactive_message(TIME_SLOTS)
                
            elif self._conversation_state == 'awaiting_reschedule':
                return MessagePayloadBuilder.create_interactive_message(TIME_SLOTS)
                
            elif self._conversation_state == 'completed':
                return MessagePayloadBuilder.create_interactive_message(
                    SELECTED_SLOT,
                    slot=self._selected_time_slot
                )
                
            logger.error(f"Invalid state for message: {self._conversation_state}")
            return MessagePayloadBuilder.create_interactive_message(
                body_text=GENERAL['error']
            )

        except Exception as e:
            logger.error(f"Error getting next message: {str(e)}")
            return MessagePayloadBuilder.create_interactive_message(
                body_text=GENERAL['error']
            )

    def _handle_initial_state(self, user_input: str) -> str:
        """Handle service type selection"""
        if user_input in ['אריזת הבית', 'סידור בבית החדש', 'ליווי מלא - אריזה וסידור']:
            self._service_type = {
                'אריזת הבית': 'packing_only',
                'סידור בבית החדש': 'unpacking_only',
                'ליווי מלא - אריזה וסידור': 'both'
            }.get(user_input)
            return 'awaiting_packing_choice'
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
        if user_input == 'דלג':
            return 'awaiting_slot_selection'
        elif self._validator.validate_photo(user_input):
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