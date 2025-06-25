"""Message payload builder for creating standardized message payloads."""
from typing import Dict, Any, List, Optional

class MessagePayloadBuilder:
    """Builds message payloads for different types of messages."""

    @staticmethod
    def create_interactive_message(
        recipient: str,
        body_text: str,
        header_text: str = None,
        footer_text: str = None,
        buttons: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """Create an interactive message payload

        Args:
            recipient (str): The recipient's phone number
            body_text (str): Message body text (required)
            header_text (str, optional): Message header text
            footer_text (str, optional): Message footer text
            buttons (List[Dict[str, str]], optional): List of button objects with 'id' and 'title'

        Raises:
            ValueError: If buttons are provided but missing required fields
            ValueError: If body_text is empty

        Returns:
            Dict[str, Any]: Message payload dictionary
        """
        if not body_text:
            raise ValueError("body_text is required for interactive messages")
            
        if buttons:
            for button in buttons:
                if 'id' not in button or 'title' not in button:
                    raise ValueError("Each button must have 'id' and 'title' fields")
        """Create an interactive message payload

        Args:
            recipient (str): The recipient's phone number
            body_text (str, optional): Message body text
            header_text (str, optional): Message header text
            footer_text (str, optional): Message footer text
            buttons (List[Dict[str, str]], optional): Interactive buttons

        Returns:
            Dict[str, Any]: Message payload dictionary
        """
        # Create payload according to schema
        payload = {
            "messaging_product": "whatsapp",
            "type": "button", # Default type for interactive messages
            "to": recipient,
            "body": {
                "text": body_text
            },
            "header": {
                "text": header_text if header_text else ""
            },
            "footer": {
                "text": footer_text if footer_text else ""
            },
            "action": {
                "buttons": [
                    {
                        "type": "quick_reply",  # From allowed enum values
                        "title": btn["title"],
                        "id": btn["id"]
                    } for btn in buttons
                ] if buttons else []  # Empty buttons array if none provided
            }
        }
            
        return payload

    @staticmethod
    def create_text_message(recipient: str, body_text: str) -> Dict[str, Any]:
        """Create a text message payload

        Args:
            recipient (str): The recipient's phone number
            body_text (str): The message text

        Returns:
            Dict[str, Any]: Message payload dictionary
        """
        return {
            "messaging_product": "whatsapp",
            "to": recipient,
            "body": body_text,
            "no_link_preview": True  # Equivalent to preview_url: False
        }