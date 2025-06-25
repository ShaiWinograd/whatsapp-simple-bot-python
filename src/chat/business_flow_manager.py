"""Business flow management module."""
from typing import Optional, Dict, Set
import logging
from .state_manager import StateManager
from ..whatsapp.label_manager import LabelManager
from ..business.flows.abstract_business_flow import AbstractBusinessFlow
from ..business.messages import NAVIGATION
from ..config.whatsapp import LABELS

logger = logging.getLogger(__name__)

class InvalidStateTransitionError(Exception):
    """Raised when attempting an invalid state transition."""
    pass

class BusinessFlowManager:
    """Responsible for coordinating business flows with state and label management"""
    
    def __init__(self, state_manager: StateManager, label_manager: LabelManager):
        """Initialize business flow manager
        
        Args:
            state_manager (StateManager): Manager for business flow states
            label_manager (LabelManager): Manager for WhatsApp labels
        """
        self._state_manager = state_manager
        self._label_manager = label_manager
        self._valid_transitions = self._initialize_valid_transitions()
        
    def _initialize_valid_transitions(self) -> Dict[str, Set[str]]:
        """Initialize valid state transitions
        
        Returns:
            Dict[str, Set[str]]: Mapping of valid transitions
        """
        return {
            'initial': {'awaiting_packing_choice', 'awaiting_emergency_support'},
            'awaiting_packing_choice': {'awaiting_customer_details', 'initial', 'awaiting_emergency_support'},
            'awaiting_customer_details': {'awaiting_verification', 'initial', 'awaiting_emergency_support'},
            'awaiting_verification': {'awaiting_photos', 'awaiting_customer_details', 'initial', 'awaiting_emergency_support'},
            'awaiting_photos': {'awaiting_slot_selection', 'initial', 'awaiting_emergency_support'},
            'awaiting_emergency_support': {'completed', 'awaiting_slot_selection'},
            'awaiting_slot_selection': {'completed', 'initial', 'awaiting_emergency_support'},
            'awaiting_reschedule': {'completed', 'initial', 'awaiting_emergency_support'},
            'completed': {'awaiting_reschedule', 'initial', 'awaiting_emergency_support'}
        }
        
    def _is_valid_state_transition(self, from_state: str, to_state: str) -> bool:
        """Check if state transition is valid
        
        Args:
            from_state (str): Current state
            to_state (str): Target state
            
        Returns:
            bool: True if transition is valid
        """
        # Allow transition to initial state from any state
        if to_state == 'initial':
            return True
            
        # Allow transition to emergency support from any state
        if to_state == 'awaiting_emergency_support':
            return True
            
        # Check if transition is in valid transitions map
        valid_transitions = self._valid_transitions.get(from_state, set())
        return to_state in valid_transitions
        
    def handle_state_transition(self, user_id: str, new_state: str) -> None:
        """Handle business flow state transition and apply appropriate labels
        
        Args:
            user_id (str): Unique identifier for the user
            new_state (str): New state to transition to
            
        Raises:
            InvalidStateTransitionError: If transition is invalid
        """
        flow = self._state_manager.get_state(user_id)
        if not flow:
            logger.error(f"No active flow for user {user_id}")
            return
            
        current_state = flow.state
        
        # Validate transition
        if not self._is_valid_state_transition(current_state, new_state):
            error_msg = f"Invalid state transition from {current_state} to {new_state}"
            logger.error(error_msg)
            raise InvalidStateTransitionError(error_msg)
            
        # Update the flow's state
        flow.set_conversation_state(new_state)
        
        # Log transition
        logger.info(f"State transition for user {user_id}: {current_state} -> {new_state}")
        
        try:
            # Handle global state transitions
            if new_state == 'initial':
                self._label_manager.remove_all_labels(user_id)
                self._label_manager.apply_label(user_id, 'bot_new_conversation')
                
            elif new_state == 'awaiting_emergency_support':
                self._label_manager.remove_all_labels(user_id)
                self._label_manager.apply_label(user_id, 'waiting_urgent_support')
                
            elif new_state == 'completed':
                self._label_manager.remove_label(user_id, 'bot_new_conversation')
                self._label_manager.apply_label(user_id, 'waiting_call_before_quote')
                
            # Apply flow-specific labels
            flow_name = flow.get_flow_name().lower()
            if flow_name in ['moving', 'organization'] and new_state != 'initial':
                self._label_manager.apply_label(user_id, flow_name)
                
        except Exception as e:
            logger.error(f"Error managing labels for user {user_id}: {str(e)}")
            raise
            
    def handle_support_request(self, user_id: str) -> None:
        """Handle an emergency support request
        
        Args:
            user_id (str): Unique identifier for the user
        """
        try:
            # Clear existing labels and apply urgent support label
            self._label_manager.remove_all_labels(user_id)
            self._label_manager.apply_label(user_id, 'waiting_urgent_support')
            
            # Update flow state if exists
            flow = self._state_manager.get_state(user_id)
            if flow:
                flow.set_conversation_state('awaiting_emergency_support')
                logger.info(f"User {user_id} requested emergency support")
                
        except Exception as e:
            logger.error(f"Error handling support request for user {user_id}: {str(e)}")
            raise