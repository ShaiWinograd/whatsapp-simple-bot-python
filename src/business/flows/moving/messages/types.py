"""Type definitions for WhatsApp message responses.

This module defines TypedDict classes for various message response structures
to ensure type safety and consistent message formatting.
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

class ConfirmationMessage(TypedDict):
    """Structure for confirmation messages."""
    header: str
    body_template: str
    footer: str
    change_slot_button: str

class ServiceResponse(TypedDict):
    """Service identification."""
    name: str

class NavigationOptions(TypedDict):
    """Standard navigation buttons."""
    back_to_main: str
    talk_to_representative: str

class SchedulingOptions(TypedDict):
    """Scheduling-related message structure."""
    header: str
    title: str
    footer: str

class DetailsTemplate(ButtonMessage):
    """Template for collecting user details."""
    address_type: str

class MovingResponseCollection(TypedDict):
    """Complete collection of moving service responses."""
    initial: ButtonMessage
    details_collection: Dict[str, ButtonMessage]
    verify_details: MessageWithOptions
    photo_requirement: MessageWithOptions
    completed: Dict[str, str]
    verify: BaseMessage
    photos: BaseMessage
    scheduling: BaseMessage
    fallback: BaseMessage
    rewrite_details: ButtonMessage
    emergency_support: ButtonMessage
    time_slots: ButtonMessage
    selected_slot: ButtonMessage
    urgent_support_message: str
    service_name: str