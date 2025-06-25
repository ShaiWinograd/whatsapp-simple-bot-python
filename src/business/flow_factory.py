from typing import Optional

from .flows.abstract_business_flow import AbstractBusinessFlow
from .flows.moving_flow import MovingFlow
from .flows.organization_flow import OrganizationFlow

class BusinessFlowFactory:
    """Factory for creating business flow instances"""
    
    @staticmethod
    def create_flow(flow_type: str) -> Optional[AbstractBusinessFlow]:
        """Create a business flow instance based on type
        
        Args:
            flow_type (str): Type of business flow to create
            
        Returns:
            Optional[AbstractBusinessFlow]: Business flow instance if type exists, None otherwise
        """
        flow_type = flow_type.lower()
        
        if flow_type == 'moving':
            return MovingFlow()
        elif flow_type == 'organization':
            return OrganizationFlow()
            
        # Additional flow types will be added here
        # elif flow_type == 'consultation':
        #     return ConsultationFlow()
            
        return None
        
    @staticmethod
    def get_available_flows() -> list[str]:
        """Get list of available business flow types
        
        Returns:
            list[str]: List of available flow types
        """
        return ['moving', 'organization']  # Add new flows to this list as they're implemented