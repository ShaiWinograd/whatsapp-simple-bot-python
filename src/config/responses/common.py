"""Common response configurations.

This module contains message templates and configurations shared across
different service flows.
"""
from typing import Dict

WELCOME: Dict[str, str] = {
    'message': 'שלום! במה נוכל לעזור לך היום?',
    'moving_button': 'שירותי הובלה',
    'organization_button': 'שירותי ארגון וסידור'
}

NAVIGATION: Dict[str, str] = {
    'back_to_main': 'חזרה לתפריט הראשי',
    'talk_to_representative': 'שיחה עם נציג'
}

GENERAL: Dict[str, str] = {
    'back_confirmation': 'בוצע, חוזרים לתפריט הראשי',
    'representative_redirect': 'מעביר אותך לשיחה עם נציג...',
    'error': 'מצטערים, אירעה שגיאה. אנא נסו שוב או פנו לנציג שירות.',
    'invalid_input': 'מצטערים, הקלט אינו תקין. אנא נסו שוב.'
}

__all__ = ['WELCOME', 'NAVIGATION', 'GENERAL']