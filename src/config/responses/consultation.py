"""Consultation service responses."""
from .common import NAVIGATION, SCHEDULING

INITIAL = {
    'header': 'ייעוץ אישי 💫',
    'welcome': 'אשמח לקיים איתך שיחת ייעוץ! על מה היית רוצה לדבר?',
    'footer': 'כאן בשבילך לכל שאלה ובקשה! 🌟',
    'options': {
        'title': 'בחר/י נושא:',
        'buttons': [
            'תכנון מעבר דירה',
            'ארגון הבית',
            'עיצוב הבית',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

QUESTIONS = {
    'question': 'האם יש שאלות ספציפיות שהיית רוצה שנדבר עליהן בשיחה?'
}

CONSULTATION_TYPE = {
    'question': 'איך היית מעדיף/ה לקיים את הפגישה?',
    'options': {
        'title': 'בחר/י:',
        'buttons': [
            'פגישה פרונטלית',
            'שיחת וידאו',
            'שיחת טלפון',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

COMPLETION = {
    'header': 'תודה על פנייתך! 💫',
    'final': 'מעולה! אשמח לקבוע איתך את שיחת הייעוץ. פגישת ייעוץ ראשונית היא ללא עלות ונמשכת כ-45 דקות.',
    'footer': 'בדרך לפתרונות מותאמים אישית! ⭐',
    'schedule': {
        **SCHEDULING,
        'buttons': [
            'בימי ראשון-שלישי',
            'בימי רביעי-חמישי',
            'ביום שישי',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

# Export all responses
RESPONSES = {
    'initial': INITIAL,
    'awaiting_questions': QUESTIONS,
    'awaiting_consultation_type': CONSULTATION_TYPE,
    'completed': COMPLETION
}