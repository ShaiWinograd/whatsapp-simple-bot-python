"""Services module for handling different conversation flows."""
from typing import Optional, Dict, Type
from .base_service import BaseConversationService
from .moving_service import MovingService
from .organization_service import OrganizationService
from .design_service import DesignService
from .consultation_service import ConsultationService
from .human_service import HumanSupportService
from .service_factory import ServiceFactory, ServiceType

# Register services with the factory
ServiceFactory.register(ServiceType.MOVING, MovingService)
ServiceFactory.register(ServiceType.ORGANIZATION, OrganizationService)
ServiceFactory.register(ServiceType.HUMAN_SUPPORT, HumanSupportService)


def create_service(service_name: str, recipient: str) -> Optional[BaseConversationService]:
    """
    Factory function to create appropriate service instance.
    
    Args:
        service_name (str): Name of the service to create
        recipient (str): Recipient's phone number
        
    Returns:
        Optional[BaseConversationService]: Service instance if service_name is valid,
                                         None otherwise
    """
    service_class = SERVICE_MAP.get(service_name)
    if service_class:
        return service_class(recipient)
    return None


__all__ = [
    'BaseConversationService',
    'MovingService',
    'OrganizationService',
    'HumanSupportService',
    'create_service'
]