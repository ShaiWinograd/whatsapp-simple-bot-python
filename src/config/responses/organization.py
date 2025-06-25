"""Organization service response configurations.

This module contains all message templates and configurations specific to
the organization service flow.
"""
from typing import Dict
from .types import (
    ButtonMessage,
    MessageWithOptions,
    BaseMessage,
    ServiceResponse,
    OrganizationResponseCollection
)
from .common import NAVIGATION

# Initial service selection
INITIAL: ButtonMessage = {
    'header': 'ארגון וסידור הבית',
    'body': "נשמח לעזור לכם לארגן ולסדר את הבית!\nבמה נוכל לסייע?",
    'footer': '',
    'buttons': [
        'סידור וארגון כללי',
        'סידור ארונות',
        'סידור מטבח',
        NAVIGATION['back_to_main'],
        NAVIGATION['talk_to_representative']
    ]
}

# Details verification
VERIFY_DETAILS: MessageWithOptions = {
    'header': 'אימות פרטים',
    'body': """אלו הפרטים שקיבלנו ממך:

{details}

האם הפרטים נכונים?""",
    'footer': '',
    'options': {
        'title': 'האם הפרטים נכונים?',
        'buttons': [
            'כן, הפרטים נכונים',
            'לא, צריך לתקן',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

# Service completion messages
COMPLETION: Dict[str, str] = {
    'success': """תודה שפנית אלינו!
נציג שלנו יצור איתך קשר בהקדם לתיאום הפגישה."""
}

FALLBACK: BaseMessage = {
    'header': 'הפניה התקבלה',
    'body': 'תודה על פנייתך! נציג מהצוות שלנו יצור איתך קשר בהקדם.',
    'footer': ''
}

SERVICE: ServiceResponse = {
    'name': 'ארגון וסידור הבית'
}

# Export all responses with type safety
SERVICE_RESPONSES = {
    'organization': {
        'initial': INITIAL,
        'verify_details': VERIFY_DETAILS,
        'completed': COMPLETION,
        'fallback': FALLBACK,
        'service_name': SERVICE['name']
    }
}

__all__ = [
    'SERVICE_RESPONSES',
    'SERVICE',
    'INITIAL',
    'VERIFY_DETAILS',
    'COMPLETION',
    'FALLBACK'
]