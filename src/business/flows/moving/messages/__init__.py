"""Message templates for the moving service flow.

This package contains all response templates and type definitions specific to
the moving service interaction flow.
"""
from .types import *
from .responses import (
    RESPONSES,
    SERVICE,
    TIME_SLOTS,
    SELECTED_SLOT,
    EMERGENCY_SUPPORT,
    INITIAL,
    DETAILS_COLLECTION,
    VERIFY_DETAILS,
    VERIFY,
    PHOTOS
)

# For backward compatibility
URGENT_SUPPORT_MESSAGE = RESPONSES['urgent_support_message']

__all__ = [
    'RESPONSES',
    'SERVICE',
    'TIME_SLOTS',
    'SELECTED_SLOT',
    'EMERGENCY_SUPPORT',
    'INITIAL',
    'DETAILS_COLLECTION',
    'VERIFY_DETAILS',
    'VERIFY',
    'PHOTOS',
    'URGENT_SUPPORT_MESSAGE'
]