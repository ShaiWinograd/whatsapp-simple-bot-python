"""Message payload builder for creating standardized message payloads."""
from typing import Dict, Any, List, Optional

class MessagePayloadBuilder:
    """Builds message payloads for different types of messages."""

    @staticmethod
    def create_message(
        recipient: str,
        body_text: str = None,
        header_text: str = None,
        footer_text: str = None,
        buttons: List[Dict[str, str]] = None
    ) -> Dict[str, Any]:
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
        payload = {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": recipient,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": body_text} if body_text else None,
                "header": {"type": "text", "text": header_text} if header_text else None,
                "footer": {"text": footer_text} if footer_text else None,
                "action": {
                    "buttons": buttons
                } if buttons else None
            }
        }
        
        # Remove None values
        if not payload["interactive"]["body"]:
            del payload["interactive"]["body"]
        if not payload["interactive"]["header"]:
            del payload["interactive"]["header"]
        if not payload["interactive"]["footer"]:
            del payload["interactive"]["footer"]
            
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
            "recipient_type": "individual",
            "to": recipient,
            "type": "text",
            "text": {
                "preview_url": False,
                "body": body_text
            }
        }