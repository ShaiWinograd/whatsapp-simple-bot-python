"""Message validation utilities."""
from typing import Dict, Any
from ..config.responses import DEBUG_PHONE_NUMBER
from ..utils.validators import validate_sender


class MessageValidator:
    """Validator for incoming WhatsApp messages."""

    @staticmethod
    def validate_message(message: Dict[str, Any]) -> bool:
        """
        Validate incoming message.
        
        Args:
            message (Dict[str, Any]): The incoming message to validate
            
        Returns:
            bool: True if message is valid, False otherwise
        """
        # Check basic message structure
        if not validate_sender(message):
            return False

        sender_number = message.get('from', '').strip()
        
        # Only process messages from the debug phone number
        if sender_number != DEBUG_PHONE_NUMBER:
            return False

        return True