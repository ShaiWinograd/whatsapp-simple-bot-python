"""Models package for WhatsApp bot application webhook payloads and data structures."""

from .webhook_payload import (
    BaseWebhookPayload,
    TextMessagePayload,
    MediaMessagePayload,
    InteractiveMessagePayload
)

__all__ = [
    'BaseWebhookPayload',
    'TextMessagePayload',
    'MediaMessagePayload',
    'InteractiveMessagePayload'
]