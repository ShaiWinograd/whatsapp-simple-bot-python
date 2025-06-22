"""Utilities for handling interactive messages."""
from typing import Dict, Any, Optional


def get_button_title(message: Dict[str, Any]) -> Optional[str]:
    """
    Extract button title from an interactive message.
    
    Args:
        message (Dict[str, Any]): The incoming message
        
    Returns:
        Optional[str]: The button title if found, None otherwise
    """
    print(f"DEBUG - Interactive message content: {message}")
    if 'interactive' in message:
        interactive = message.get('interactive', {})
        print(f"DEBUG - Interactive part: {interactive}")
        button_reply = interactive.get('button_reply', {})
        print(f"DEBUG - Button reply: {button_reply}")
        title = button_reply.get('title')
        print(f"DEBUG - Extracted title from interactive: {title}")
        return title
    elif 'reply' in message and message.get('reply', {}).get('type') == 'buttons_reply':
        buttons_reply = message.get('reply', {}).get('buttons_reply', {})
        print(f"DEBUG - Buttons reply: {buttons_reply}")
        title = buttons_reply.get('title')
        print(f"DEBUG - Extracted title from buttons_reply: {title}")
        return title
    return None