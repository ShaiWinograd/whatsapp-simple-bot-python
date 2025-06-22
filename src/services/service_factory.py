from enum import Enum
from typing import Type, Dict

from src.services.base_service import BaseConversationService

class ServiceType(Enum):
    ORGANIZATION = "organization"
    DESIGN = "design"
    CONSULTATION = "consultation"
    MOVING = "moving"
    OTHER = "other"

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
    def create(cls, service_type: ServiceType, recipient: str) -> BaseConversationService:
        """Create an instance of the requested service type.
        Args:
            service_type (ServiceType): The type of service to create.
            recipient (str): The recipient's phone number.
        Returns:
            BaseConversationService: An instance of the requested service type.
        Raises:
            ValueError: If the service type is not registered.
        """
        service_class = cls._services.get(service_type)
        if not service_class:
            raise ValueError(f"Unknown service type: {service_type}")
        return service_class(recipient)