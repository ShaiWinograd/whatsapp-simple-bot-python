"""Type definitions for service responses.

This module defines TypedDict classes for various message response structures
to ensure type safety and consistent message formatting across services.
"""
from typing import TypedDict, List, Dict

class BaseMessage(TypedDict):
    """Base message structure with header, body, and footer."""
    header: str
    body: str
    footer: str

class ButtonMessage(BaseMessage):
    """Message with button options."""
    buttons: List[str]

class OptionsMessage(TypedDict):
    """Structure for option selections."""
    title: str
    buttons: List[str]

class MessageWithOptions(BaseMessage):
    """Message that includes option selections."""
    options: OptionsMessage

class ServiceResponse(TypedDict):
    """Service identification."""
    name: str

class OrganizationResponseCollection(TypedDict):
    """Complete collection of organization service responses."""
    initial: ButtonMessage
    verify_details: MessageWithOptions
    completed: Dict[str, str]
    fallback: BaseMessage
    service_name: str

__all__ = [
    'BaseMessage',
    'ButtonMessage',
    'OptionsMessage',
    'MessageWithOptions',
    'ServiceResponse',
    'OrganizationResponseCollection'
]