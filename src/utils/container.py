from dependency_injector import containers, providers
from src.conversation_manager import ConversationManager
from src.services.service_factory import ServiceFactory

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    conversation_manager = providers.Singleton(
        ConversationManager,
        timeout_minutes=config.conversation.timeout_minutes
    )
    
    service_factory = providers.Singleton(
        ServiceFactory
    )