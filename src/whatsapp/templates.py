"""WhatsApp message templates and defaults.

This module contains default message templates and options used by the WhatsApp
message builder for constructing messages.
"""
from typing import Dict, List

# General message templates
GENERAL: Dict[str, str | List[str]] = {
    'intro': 'שלום!\nהגעתם לעוזר הדיגיטלי של S&O.\nאני כאן לעזור לכם למצוא את השירות המתאים ולענות על כל שאלה.\nלנוחותכם, בכל שלב ניתן לחזור לתפריט הראשי או לשוחח עם נציג/ה באמצעות הכפתורים בתחתית.',
    'header': 'ברוכים הבאים לSpace & Order',
    'welcome_message': 'בתור התחלה, אנא בחרו את השירות בו אתם מתעניינים:',
    'footer': '',
    'options': [
        'מעבר דירה',
        'סידור וארגון הבית',
        'אחר',
        'שיחה עם נציג/ה'
    ],
    'error': 'מצטערים, לא הצלחנו להבין את ההודעה. האם תוכל/י לנסח אותה מחדש?'
}