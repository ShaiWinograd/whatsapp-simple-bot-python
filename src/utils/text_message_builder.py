"""Utility for building text messages."""
from typing import Dict, Any
from ..models.webhook_payload import TextMessagePayload


def create_text_message(
    recipient: str,
    body_text: str
) -> Dict[str, Any]:
    """
    Create a text message payload.
    
    Args:
        recipient (str): The recipient's phone number
        body_text (str): The message text content
    
    Returns:
        Dict[str, Any]: The text message payload
    """
    print("\nCreating text payload for recipient:", recipient)
    print("Using body:", body_text)
    
    text_payload = TextMessagePayload(
        to=recipient,
        body=body_text
    )
    
    payload = text_payload.to_dict()
    print("Final payload:", payload)
    return payload