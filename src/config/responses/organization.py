"""Organization service responses."""
from .common import NAVIGATION, SCHEDULING

INITIAL = {
    'header': 'שירות ארגון וסידור הבית',
    'welcome': 'ברוכים הבאים לשירות הארגון המקצועי שלנו! איזה חלל בבית נעזור לך להפוך למסודר ונעים יותר?',
    'footer': '',
    'options': {
        'title': 'בחר/י את החלל הרצוי:',
        'buttons': [
            'חדר שינה וארונות בגדים',
            'מטבח ואזורי אחסון',
            'משרד ביתי',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

PAIN_POINTS = {
    'question': 'ספר/י לנו מה הכי מאתגר אותך במצב הנוכחי? איזה שינויים היית רוצה לראות?'
}

TIMING = {
    'question': 'מתי נוח לך להתחיל בתהליך השינוי?',
    'options': {
        'title': 'בחר/י את המועד המועדף:',
        'buttons': [
            'בשבוע הקרוב',
            'בחודש הקרוב',
            'בעתיד, רק מתעניין/ת',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

COMPLETION = {
    'header': 'מוכנים להתחיל?',
    'final': 'נהדר! הצעד הראשון הוא פגישת ייעוץ חינמית בה נכיר את המרחב שלך ונבנה יחד תכנית פעולה מותאמת אישית. נשמח לקבוע פגישה!',
    'footer': '',
    'schedule': {
        **SCHEDULING,
        'buttons': [
            'בוקר',
            'צהריים',
            'ערב',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

# Export all responses
RESPONSES = {
    'initial': INITIAL,
    'awaiting_pain_points': PAIN_POINTS,
    'awaiting_timing': TIMING,
    'completed': COMPLETION
}