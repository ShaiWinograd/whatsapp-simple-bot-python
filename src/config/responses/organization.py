"""Organization service responses."""
from .common import NAVIGATION, SCHEDULING

INITIAL = {
    'header': 'שירות ארגון וסידור הבית ✨',
    'welcome': 'אשמח לעזור לך לארגן ולסדר! איזה חלל צריך עזרה?',
    'footer': 'יחד נהפוך כל חלל למאורגן ונעים! 🏡',
    'options': {
        'title': 'בחר/י מהאפשרויות:',
        'buttons': [
            'חדר שינה/ארון בגדים',
            'מטבח',
            'משרד ביתי',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

PAIN_POINTS = {
    'question': 'מה מפריע לך במצב הנוכחי? מה היית רוצה לשפר?'
}

TIMING = {
    'question': 'מתי היית רוצה להתחיל בתהליך?',
    'options': {
        'title': 'בחר/י:',
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
    'header': 'מוכנים להתחיל? ✨',
    'final': 'נשמע מעולה! אשמח להיפגש לפגישת ייעוץ ללא עלות כדי להכיר את המרחב ולהציע פתרונות מותאמים אישית. האם תרצה/י לקבוע פגישה?',
    'footer': 'בדרך לבית מאורגן ומסודר! 🏡',
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