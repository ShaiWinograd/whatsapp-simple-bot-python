"""Chat package for WhatsApp bot application.

This package contains core chat functionality components:
- ConversationManager: Manages user conversations and their states
- MessageHandler: Processes incoming messages and generates appropriate responses
"""

from .conversation_manager import ConversationManager
from .message_handler import MessageHandler

__all__ = ['ConversationManager', 'MessageHandler']