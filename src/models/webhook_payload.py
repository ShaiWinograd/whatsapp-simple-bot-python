from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List, Union

@dataclass
class MessageHeader:
    """Header for interactive messages."""
    type: str
    text: Optional[str] = None  # For text headers
    image: Optional[Dict[str, str]] = None  # For image headers with URL
    document: Optional[Dict[str, str]] = None  # For document headers with URL
    video: Optional[Dict[str, str]] = None  # For video headers with URL

@dataclass
class MessageFooter:
    """Footer for interactive messages."""
    text: str

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
            "body": {"text": self.body}
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
    """Payload for interactive button messages."""
    body_text: str
    header: Optional[MessageHeader] = None
    footer: Optional[MessageFooter] = None
    buttons: List[Dict[str, str]] = field(default_factory=list)  # List of {id, title} dicts
    type: str = field(default="button")

    def to_dict(self) -> Dict[str, Any]:
        """Convert to WhatsApp API format."""
        payload = super().to_dict()

        # Add body as string
        payload["body"] = {"text": self.body_text}

        # Optional header
        if self.header:
            payload["header"] = {
                "type": self.header.type,
                **({k: v for k, v in {
                    "text": self.header.text,
                    "image": self.header.image,
                    "document": self.header.document,
                    "video": self.header.video
                }.items() if v is not None})
            }

        # Optional footer
        if self.footer:
            payload["footer"] = {"text": self.footer.text}

        # Add type field
        payload["type"] = self.type

        # Required buttons under action
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
