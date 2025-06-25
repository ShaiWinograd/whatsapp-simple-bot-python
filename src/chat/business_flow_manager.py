from typing import Optional
from .state_manager import StateManager
from .label_manager import LabelManager
from ..business.flows.abstract_business_flow import AbstractBusinessFlow

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
        
    def handle_state_transition(self, user_id: str, new_state: str) -> None:
        """Handle business flow state transition and apply appropriate labels
        
        Args:
            user_id (str): Unique identifier for the user
            new_state (str): New state to transition to
        """
        flow = self._state_manager.get_state(user_id)
        if not flow:
            return
            
        # Update the flow's state
        flow.set_conversation_state(new_state)
        
        # Handle global state transitions
        if new_state == 'initial':
            self._label_manager.remove_all_labels(user_id)
            self._label_manager.apply_label(user_id, 'bot_new_conversation')
            
        elif new_state == 'awaiting_emergency_support':
            self._label_manager.apply_label(user_id, 'waiting_urgent_support')
            
        elif new_state == 'completed':
            self._label_manager.apply_label(user_id, 'waiting_call_before_quote')
            
        # Apply flow-specific labels
        flow_name = flow.get_flow_name().lower()
        if flow_name in ['moving', 'organization']:
            self._label_manager.apply_label(user_id, flow_name)
            
    def handle_support_request(self, user_id: str) -> None:
        """Handle an emergency support request
        
        Args:
            user_id (str): Unique identifier for the user
        """
        # Clear existing labels and apply urgent support label
        self._label_manager.remove_all_labels(user_id)
        self._label_manager.apply_label(user_id, 'waiting_urgent_support')
        
        # Update flow state if exists
        flow = self._state_manager.get_state(user_id)
        if flow:
            flow.set_conversation_state('awaiting_emergency_support')