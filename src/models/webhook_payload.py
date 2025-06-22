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
    body: str
    button_messages: List[str]

    def to_dict(self) -> Dict[str, Any]:
        payload = super().to_dict()
        buttons = []
        for i, msg in enumerate(self.button_messages):
            buttons.append({
                "type": "quick_reply",
                "title": msg,
                "id": str(i)
            })

        payload.update({
            "type": "button",
            "header": {
                "text": "השירותים שלנו"
            },
            "body": {
                "text": self.body
            },
            "footer": {
                "text": "בחר.י אחת מהאפרויות על מנת להתקדם"
            },
            "action": {
                "buttons": buttons
            }
        })
        return payload
