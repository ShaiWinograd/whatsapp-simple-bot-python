from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class BaseWebhookPayload:
    """Base class for all webhook payloads with common fields."""
    to: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert payload to dictionary format."""
        return {
            "to": self.to,
        }

@dataclass
class TextMessagePayload(BaseWebhookPayload):
    """Payload for text messages."""
    body: str

    def to_dict(self) -> Dict[str, Any]:
        payload = super().to_dict()
        payload["body"] = self.body
        return payload

@dataclass
class MediaMessagePayload(BaseWebhookPayload):
    """Payload for media messages (images, videos, documents)."""
    media_url: str
    caption: Optional[str] = field(default=None)
    filename: Optional[str] = field(default=None)

    def to_dict(self) -> Dict[str, Any]:
        payload = super().to_dict()
        payload.update({
            "media": {
                "url": self.media_url,
                "caption": self.caption,
                "filename": self.filename
            }
        })
        return {k: v for k, v in payload.items() if v is not None}

@dataclass
class InteractiveMessagePayload(BaseWebhookPayload):
    """Payload for interactive messages with buttons."""
    body_text: str
    header_text: Optional[str] = None
    footer_text: Optional[str] = None
    buttons: List[Dict[str, str]] = field(default_factory=list)  # List of {id, title} dicts

    def to_dict(self) -> Dict[str, Any]:
        """Convert to WhatsApp API format."""
        payload = super().to_dict()
        
        payload.update({
            "type": "button",  # Root level type must be: list, button, or product
            "body": {
                "text": self.body_text
            }
        })

        # Add optional header
        if self.header_text:
            payload["header"] = {
                "type": "text",
                "text": self.header_text
            }

        # Add optional footer
        if self.footer_text:
            payload["footer"] = {
                "text": self.footer_text
            }

        # Add buttons if present
        if self.buttons:
            print("Creating button payload with buttons:", self.buttons)
            buttons = [
                {
                    "type": "quick_reply",
                    "id": str(button["id"]),
                    "title": button["title"]
                }
                for button in self.buttons
            ]
            print("Final button structure:", buttons)
            payload["action"] = {
                "buttons": buttons
            }
            print("Final payload structure:", payload)

        return payload
