"""Utility for building interactive messages."""
from typing import Dict, Any, List, Optional
from ..models.webhook_payload import InteractiveMessagePayload
from ..config.responses.common import GENERAL

def create_interactive_message(
    recipient: str,
    body_text: str = None,
    header_text: str = None,
    footer_text: str = None,
    buttons: List[Dict[str, str]] = None
) -> Dict[str, Any]:
    """
    Create an interactive message payload with buttons.
    
    Args:
        recipient (str): The recipient's phone number
        body_text (str, optional): Custom body text. Defaults to welcome message.
        header_text (str, optional): Custom header text. Defaults to welcome header.
        footer_text (str, optional): Custom footer text. Defaults to welcome footer.
        buttons (List[Dict[str, str]], optional): Custom buttons. Defaults to main menu options.
    
    Returns:
        Dict[str, Any]: The interactive message payload
    """
    print("\nCreating interactive payload for recipient:", recipient)
    
    # Use provided values or defaults from GENERAL
    # Combine intro and welcome message if using defaults
    body = body_text or f"{GENERAL['intro']}\n\n{GENERAL['welcome_message']}"
    header = header_text or GENERAL['header']
    footer = footer_text if footer_text is not None else ''
    button_list = buttons or [
        {"id": str(i), "title": title}
        for i, title in enumerate(GENERAL['options'])
    ]

    print("Using body:", body)
    print("Using header:", header)
    print("Using footer:", footer)
    print("Using buttons:", button_list)

    # Create and return payload
    payload = InteractiveMessagePayload(
        to=recipient,
        body_text=body,
        header_text=header,
        footer_text=footer,
        buttons=button_list
    ).to_dict()
    print("Final payload:", payload)
    return payload