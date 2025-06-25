"""Common message templates and utilities used across business flows.

This module provides shared message templates, navigation options, and utility
functions for creating consistent message structures across different flows.
"""
from typing import Dict

from src.config.responses.common import NAVIGATION
from .flows.moving.messages.types import (
    ButtonMessage,
    DetailsTemplate
)

# Error messages
ERROR_MESSAGES: Dict[str, str] = {
    'general': 'מצטערים, לא הצלחנו להבין את ההודעה. האם תוכל/י לנסח אותה מחדש?',
    'validation': 'נראה שחסרים חלק מהפרטים הנדרשים. אנא נסה/י שוב.',
    'system': 'מצטערים, התרחשה שגיאה. אנא נסה/י שוב או צור/י קשר עם נציג.'
}

# Base template for collecting user details
DETAILS_BASE_TEMPLATE = """כדי שנוכל לנוודא שאנחנו זמינים בתאריך המעבר ושאתם גרים שלכם נמצאת בטווח השירות שלנו.
אנא אנא שלחו בהודעה חוזרת את כל הפרטים הבאים:

שם מלא
{address_type}
כתובת מייל
תאריך הובלה מתוכנן

אם טרם נקבע תאריך הובלה, ציינו תאריך משוער"""

def create_details_message(title: str, address_type: str) -> DetailsTemplate:
    """Create a details collection message with the given title and address type.
    
    Args:
        title: Header text for the message
        address_type: Type of address to request (current/new/both)
        
    Returns:
        Formatted details collection message
    """
    return {
        'header': title,
        'body': DETAILS_BASE_TEMPLATE.format(address_type=address_type),
        'footer': '',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }

# Standard time slots for scheduling
DEFAULT_TIME_SLOTS: Dict[str, str] = {
    'today_12_14': 'היום בין 12:00-14:00',
    'today_14_16': 'היום בין 14:00-16:00',
    'today_16_18': 'היום בין 16:00-18:00',
    'tomorrow_10_12': 'מחר בין 10:00-12:00',
    'tomorrow_12_14': 'מחר בין 12:00-14:00'
}

# Template for photo/video request message
MEDIA_REQUEST_TEMPLATE: ButtonMessage = {
    'header': 'שליחת תמונות',
    'body': """כדי לעזור להעריך את היקף העבודה בצורה כמה שיותר מדוייקת, נשמח לקבל תמונות או סרטון קצר של הבית:

בבקשה שימו דגש על צילום ארונות (בגדים, מטבח ואחסון) עם דלתות פתוחות

התמונות משמשות למתן הצעת המחיר בלבד ואינן נשמרות.""",
    'footer': '',
    'buttons': [
        'מעדיפים לדלג',
        NAVIGATION['back_to_main'],
        NAVIGATION['talk_to_representative']
    ]
}