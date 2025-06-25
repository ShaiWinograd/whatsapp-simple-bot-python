from typing import Dict, List

from ..whatsapp.client import WhatsAppClient
from ..config.whatsapp import LABELS

class LabelManager:
    """Responsible for managing WhatsApp conversation labels"""
    
    def __init__(self):
        self._user_labels: Dict[str, List[str]] = {}
        
    def apply_label(self, user_id: str, label_key: str) -> None:
        """Apply a label to a conversation
        
        Args:
            user_id (str): Unique identifier for the user
            label_key (str): Key of the label to apply from LABELS dict
        """
        if label_key in LABELS and LABELS[label_key]:
            WhatsAppClient.apply_label(user_id, LABELS[label_key])
            if user_id not in self._user_labels:
                self._user_labels[user_id] = []
            if label_key not in self._user_labels[user_id]:
                self._user_labels[user_id].append(label_key)
                
    def remove_label(self, user_id: str, label_key: str) -> None:
        """Remove a label from a conversation
        
        Args:
            user_id (str): Unique identifier for the user
            label_key (str): Key of the label to remove from LABELS dict
        """
        if label_key in LABELS and LABELS[label_key]:
            WhatsAppClient.remove_label(user_id, LABELS[label_key])
            if user_id in self._user_labels:
                self._user_labels[user_id] = [l for l in self._user_labels[user_id] if l != label_key]
                
    def remove_all_labels(self, user_id: str) -> None:
        """Remove all labels from a conversation
        
        Args:
            user_id (str): Unique identifier for the user
        """
        if user_id in self._user_labels:
            for label in self._user_labels[user_id]:
                self.remove_label(user_id, label)
            self._user_labels[user_id] = []
            
    def get_user_labels(self, user_id: str) -> List[str]:
        """Get all labels for a user
        
        Args:
            user_id (str): Unique identifier for the user
            
        Returns:
            List[str]: List of label keys for the user
        """
        return self._user_labels.get(user_id, [])