"""Responses configuration package."""
from .common import GENERAL, HUMAN_SUPPORT, NAVIGATION
from .organization import RESPONSES as ORGANIZATION_RESPONSES
from .moving import RESPONSES as MOVING_RESPONSES
from .consultation import RESPONSES as CONSULTATION_RESPONSES
from .design import RESPONSES as DESIGN_RESPONSES

# Service responses mapping
SERVICE_RESPONSES = {
    'organization': ORGANIZATION_RESPONSES,
    'moving': MOVING_RESPONSES,
    'consultation': CONSULTATION_RESPONSES,
    'design': DESIGN_RESPONSES,
    'human_support': {'transfer_message': HUMAN_SUPPORT['transfer_message']}
}

# Combined responses
RESPONSES = {
    **GENERAL,
    **SERVICE_RESPONSES
}

__all__ = [
    'RESPONSES',
    'SERVICE_RESPONSES',
    'GENERAL',
    'HUMAN_SUPPORT',
    'NAVIGATION',
    'ORGANIZATION_RESPONSES',
    'MOVING_RESPONSES',
    'CONSULTATION_RESPONSES',
    'DESIGN_RESPONSES'
]