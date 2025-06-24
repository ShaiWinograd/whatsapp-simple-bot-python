from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

@dataclass
class BaseWebhookPayload:
    """Base class for all webhook payloads with common fields."""
    to: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert payload to dictionary format."""
        return {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": self.to,
        }

@dataclass
class TextMessagePayload(BaseWebhookPayload):
    """Payload for text messages."""
    body: str

    def to_dict(self) -> Dict[str, Any]:
        payload = super().to_dict()
        payload.update({
            "type": "text",
            "text": {
                "body": self.body
            }
        })
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
        payload["type"] = "interactive"

        # Required body
        payload["body"] = {"text": self.body_text}

        # Optional header
        if self.header_text:
            payload["header"] = {"text": self.header_text}

        # Optional footer
        if self.footer_text:
            payload["footer"] = {"text": self.footer_text}

        # Required action with buttons
        payload["action"] = {
            "buttons": [
                {
                    "type": "quick_reply",
                    "id": str(button["id"]),
                    "title": button["title"]
                }
                for button in self.buttons
            ]
        }

        return payload
