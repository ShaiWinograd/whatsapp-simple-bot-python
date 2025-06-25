"""WhatsApp label management functionality."""
from typing import Set

class LabelManager:
    """Manages WhatsApp chat labels."""
    
    def __init__(self):
        """Initialize label manager."""
        self._user_labels: dict[str, Set[str]] = {}
        
    def apply_label(self, user_id: str, label: str) -> None:
        """Apply a label to a user's conversation
        
        Args:
            user_id (str): Unique identifier for the user
            label (str): Label to apply
        """
        if user_id not in self._user_labels:
            self._user_labels[user_id] = set()
        self._user_labels[user_id].add(label)
        
    def remove_label(self, user_id: str, label: str) -> None:
        """Remove a specific label from a user
        
        Args:
            user_id (str): Unique identifier for the user
            label (str): Label to remove
        """
        if user_id in self._user_labels:
            self._user_labels[user_id].discard(label)
            
    def remove_all_labels(self, user_id: str) -> None:
        """Remove all labels for a user
        
        Args:
            user_id (str): Unique identifier for the user
        """
        if user_id in self._user_labels:
            del self._user_labels[user_id]
            
    def get_labels(self, user_id: str) -> Set[str]:
        """Get all labels for a user
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            Set[str]: Set of labels for the user
        """
        return self._user_labels.get(user_id, set())