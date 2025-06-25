from abc import ABC, abstractmethod
from typing import Optional, Dict, Any

class AbstractBusinessFlow(ABC):
    """Abstract class defining the contract for all business flows"""
    
    def __init__(self):
        self._conversation_state: str = 'initial'
        self._flow_data: Dict[str, Any] = {}
        
    @property
    def state(self) -> str:
        """Get current conversation state"""
        return self._conversation_state
        
    @abstractmethod
    def get_flow_name(self) -> str:
        """Get the name of this business flow
        
        Returns:
            str: Name of the flow (e.g., 'moving', 'organization')
        """
        pass
        
    def set_conversation_state(self, new_state: str) -> None:
        """Set the conversation state
        
        Args:
            new_state (str): New state to set
        """
        self._conversation_state = new_state
        
    def get_flow_data(self) -> Dict[str, Any]:
        """Get all data collected during this flow
        
        Returns:
            Dict[str, Any]: Collected flow data
        """
        return self._flow_data
        
    def set_flow_data(self, key: str, value: Any) -> None:
        """Store data collected during the flow
        
        Args:
            key (str): Data identifier
            value (Any): Value to store
        """
        self._flow_data[key] = value
        
    def get_flow_data_value(self, key: str) -> Optional[Any]:
        """Get specific data value from the flow
        
        Args:
            key (str): Data identifier
            
        Returns:
            Optional[Any]: Stored value if exists, None otherwise
        """
        return self._flow_data.get(key)
        
    @abstractmethod
    def handle_input(self, user_input: str) -> str:
        """Handle user input based on current state
        
        Args:
            user_input (str): Input from user
            
        Returns:
            str: Next state after handling input
        """
        pass
        
    @abstractmethod
    def get_next_message(self) -> str:
        """Get next message to send based on current state
        
        Returns:
            str: Message to send to user
        """
        pass