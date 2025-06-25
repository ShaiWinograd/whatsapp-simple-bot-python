from typing import Dict, Any, Optional

from .abstract_business_flow import AbstractBusinessFlow
from ...whatsapp.utils.messages import MessageBuilder, get_button_title
from ...config.responses import SERVICE_RESPONSES, GENERAL
from ...config.responses.common import NAVIGATION

class OrganizationFlow(AbstractBusinessFlow):
    """Handles the organization service business flow"""
    
    def __init__(self):
        super().__init__()
        self._states = {
            'initial': self._handle_initial_state,
            'awaiting_customer_details': self._handle_customer_details,
            'awaiting_verification': self._handle_verification,
            'completed': self._handle_completed_state
        }
        self._responses = SERVICE_RESPONSES['organization']
        self._customer_details: Optional[str] = None