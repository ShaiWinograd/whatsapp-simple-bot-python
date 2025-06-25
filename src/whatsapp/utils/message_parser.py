"""Utilities for parsing WhatsApp message content."""
from typing import Dict, Any, Optional
from ...utils.logger import setup_logger

logger = setup_logger(__name__)

def get_button_title(message: Dict[str, Any]) -> Optional[str]:
    """Extract button title from an incoming interactive message.
    
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