"""Common response configurations.

This module contains message templates and configurations shared across
different service flows.
"""
from typing import Dict

WELCOME: Dict[str, str] = {
    'message': 'שלום!'
    '\n'
    'הגעתם לעוזר הדיגיטלי של S&O.'
    '\n\n'
    'אני כאן לעזור לכם למצוא את השירות המתאים ולענות על כל שאלה.'
    '\n'
    'לנוחותכם, בכל שלב ניתן לחזור לתפריט הראשי או לשוחח עם נציגה באמצעות הכפתורים בתחתית.'
    '\n\n'
    'בתור התחלה, אנא בחרו את השירות בו אתם מעוניינים:',
    'header': 'ברוכים הבאים ל Space & Order',
    'moving_button': 'מעבר דירה',
    'organization_button': 'סידור וארגון הבית',
    'other_button': 'אחר',
}

NAVIGATION: Dict[str, str] = {
    'back_to_main': 'חזרה לתפריט הראשי',
    'talk_to_representative': 'שיחה עם נציגה'
}

GENERAL: Dict[str, str] = {
    'back_confirmation': 'בוצע, חוזרים לתפריט הראשי',
    'representative_redirect': 'מעביר אותך לשיחה עם נציג...',
    'error': 'מצטערים, אירעה שגיאה. אנא נסו שוב או פנו לנציג שירות.',
    'invalid_input': 'מצטערים, הקלט אינו תקין. אנא נסו שוב.'
}

__all__ = ['WELCOME', 'NAVIGATION', 'GENERAL']