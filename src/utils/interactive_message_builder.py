"""Utility for building interactive messages."""
from typing import Dict, Any, List, Optional, Union
from ..models.webhook_payload import (
    InteractiveMessagePayload,
    MessageHeader,
    MessageFooter
)
from ..config.responses.common import GENERAL

class InteractiveMessageBuilder:
    """Class for building interactive messages."""
    
    @staticmethod
    def create_message(
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
        # Use defaults only for body and buttons, not header/footer
        # If only recipient is provided, use all defaults
        using_defaults = body_text is None and header_text is None and footer_text is None and buttons is None
        
        body = body_text or f"{GENERAL['intro']}\n\n{GENERAL['welcome_message']}"
        header = header_text if not using_defaults else GENERAL['header']
        footer = footer_text  # Don't set default footer
        button_list = buttons or [
            {"id": str(i), "title": title}
            for i, title in enumerate(GENERAL['options'])
        ]

        print("Using body:", body)
        print("Using header:", header)
        print("Using footer:", footer)
        print("Using buttons:", button_list)

        # Create payload using InteractiveMessagePayload
        # Create header object if header text is provided
        header_obj = MessageHeader(type="text", text=header) if header else None
        
        # Create footer object if footer text is provided
        footer_obj = MessageFooter(text=footer) if footer else None
        
        interactive_payload = InteractiveMessagePayload(
            to=recipient,
            body_text=body,
            header=header_obj,
            footer=footer_obj,
            buttons=button_list,
            type="button"  # Default type for interactive messages
        )
        
        payload = interactive_payload.to_dict()
        print("Final payload:", payload)
        return payload