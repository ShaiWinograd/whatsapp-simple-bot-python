"""WhatsApp message utilities for building and parsing messages."""
from typing import Dict, Any, List, Optional

from ...models.webhook_payload import (
    InteractiveMessagePayload,
    TextMessagePayload,
    MessageHeader,
    MessageFooter
)
from ..templates import GENERAL
from ...utils.logger import setup_logger

logger = setup_logger(__name__)

class MessageBuilder:
    """Builder for creating outgoing WhatsApp messages."""
    
    @staticmethod
    def create_message(
        recipient: str,
        body_text: Optional[str] = None,
        header_text: Optional[str] = None,
        footer_text: Optional[str] = None,
        buttons: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Create an interactive message payload with buttons.
        
        Args:
            recipient (str): The recipient's phone number
            body_text (str, optional): Custom body text. Defaults to welcome message.
            header_text (str, optional): Custom header text. Defaults to welcome header.
            footer_text (str, optional): Custom footer text. No default.
            buttons (List[Dict[str, str]], optional): Custom buttons. Defaults to main menu options.
        
        Returns:
            Dict[str, Any]: The interactive message payload ready for the WhatsApp API
        """
        using_defaults = body_text is None and header_text is None and footer_text is None and buttons is None
        
        body = body_text or f"{GENERAL['intro']}\n\n{GENERAL['welcome_message']}"
        header = header_text if not using_defaults else GENERAL['header']
        footer = footer_text
        button_list = buttons or [
            {"id": str(i), "title": title}
            for i, title in enumerate(GENERAL['options'])
        ]

        header_obj = MessageHeader(type="text", text=header) if header else None
        footer_obj = MessageFooter(text=footer) if footer else None
        
        interactive_payload = InteractiveMessagePayload(
            to=recipient,
            body_text=body,
            header=header_obj,
            footer=footer_obj,
            buttons=button_list,
            type="button"
        )
        
        logger.debug("Created interactive message payload for %s", recipient)
        return interactive_payload.to_dict()

    @staticmethod
    def create_text_message(recipient: str, body_text: str) -> Dict[str, Any]:
        """
        Create a text message payload.
        
        Args:
            recipient (str): The recipient's phone number
            body_text (str): The message text content
        
        Returns:
            Dict[str, Any]: The text message payload ready for the WhatsApp API
        """
        text_payload = TextMessagePayload(
            to=recipient,
            body=body_text
        )
        
        logger.debug("Created text message payload for %s", recipient)
        return text_payload.to_dict()


def get_button_title(message: Dict[str, Any]) -> Optional[str]:
    """
    Extract button title from an incoming interactive message.
    
    Args:
        message (Dict[str, Any]): The incoming WhatsApp message payload
        
    Returns:
        Optional[str]: The selected button title if found, None otherwise
    
    Example:
        >>> msg = {"interactive": {"button_reply": {"title": "Yes"}}}
        >>> get_button_title(msg)
        'Yes'
    """
    # Handle interactive button responses
    if 'interactive' in message:
        interactive = message.get('interactive', {})
        button_reply = interactive.get('button_reply', {})
        title = button_reply.get('title')
        logger.debug("Extracted button title from interactive: %s", title)
        return title

    # Handle legacy button responses
    if 'reply' in message and message.get('reply', {}).get('type') == 'buttons_reply':
        buttons_reply = message.get('reply', {}).get('buttons_reply', {})
        title = buttons_reply.get('title')
        logger.debug("Extracted button title from buttons_reply: %s", title)
        return title

    logger.debug("No button title found in message")
    return None