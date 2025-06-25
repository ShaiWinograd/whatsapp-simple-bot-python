from typing import Dict, Any, Optional

from .abstract_business_flow import AbstractBusinessFlow
from ...utils.interactive_message_builder import InteractiveMessageBuilder
from ...utils.interactive_message_utils import get_button_title
from ...config.responses.moving import (
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
from ...config.responses.common import NAVIGATION, GENERAL

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
            'completed': self._handle_completed_state
        }
        self._service_type: Optional[str] = None
        self._selected_time_slot: Optional[str] = None
        self._customer_details: Optional[str] = None