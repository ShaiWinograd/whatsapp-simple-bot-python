from enum import Enum
from typing import Type, Dict

from src.services.base_service import BaseConversationService
from src.utils.errors import ConversationError

class ServiceType(Enum):
    ORGANIZATION = "organization"
    MOVING = "moving"
    HUMAN_SUPPORT = "human_support"

class ServiceFactory:
    _services: Dict[ServiceType, Type[BaseConversationService]] = {}
    
    @classmethod
    def register(cls, service_type: ServiceType, service_class: Type[BaseConversationService]) -> None:
        """Register a new service class with the factory.
        Args:
            service_type (ServiceType): The type of service to register.
            service_class (Type[BaseConversationService]): The service class to register.
        """
        cls._services[service_type] = service_class
    
    @classmethod
    def create(cls, service_type: ServiceType, recipient: str, conversation_manager=None) -> BaseConversationService:
        """Create an instance of the requested service type.
        Args:
            service_type (ServiceType): The type of service to create.
            recipient (str): The recipient's phone number.
            conversation_manager: Optional conversation manager instance.
        Returns:
            BaseConversationService: An instance of the requested service type.
        Raises:
            ConversationError: If the service type is not registered or service creation fails.
        """
        try:
            service_class = cls._services.get(service_type)
            if not service_class:
                raise ValueError(f"Unknown service type: {service_type}")
            return service_class(recipient, conversation_manager)
        except Exception as e:
            raise ConversationError(f"Failed to create service: {str(e)}")