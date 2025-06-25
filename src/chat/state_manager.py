from typing import Dict, Optional

from ..business.flows.abstract_business_flow import AbstractBusinessFlow

class StateManager:
    """Responsible for managing business flow states"""
    
    def __init__(self):
        """Initialize state manager"""
        self._states: Dict[str, AbstractBusinessFlow] = {}
        
    def set_state(self, user_id: str, flow: AbstractBusinessFlow) -> None:
        """Set the business flow for a user
        
        Args:
            user_id (str): Unique identifier for the user
            flow (AbstractBusinessFlow): The business flow instance
        """
        self._states[user_id] = flow
        
    def get_state(self, user_id: str) -> Optional[AbstractBusinessFlow]:
        """Get the current business flow for a user
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            Optional[AbstractBusinessFlow]: The current flow if exists, None otherwise
        """
        return self._states.get(user_id)
        
    def remove_state(self, user_id: str) -> None:
        """Remove the business flow for a user
        
        Args:
            user_id (str): Unique identifier for the user
        """
        self._states.pop(user_id, None)
        
    def get_flow_state(self, user_id: str) -> Optional[str]:
        """Get the current state of a user's business flow
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            Optional[str]: Current state if flow exists, None otherwise
        """
        flow = self.get_state(user_id)
        return flow.state if flow else None
        
    def has_active_flow(self, user_id: str) -> bool:
        """Check if a user has an active business flow
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            bool: True if user has an active flow, False otherwise
        """
        return user_id in self._states