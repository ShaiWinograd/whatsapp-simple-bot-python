class WhatsAppBotError(Exception):
    """Base exception for WhatsApp bot errors"""
    pass

class ServiceCreationError(WhatsAppBotError):
    """Raised when service creation fails"""
    pass

class ConversationError(WhatsAppBotError):
    """Raised for conversation-related errors"""
    pass