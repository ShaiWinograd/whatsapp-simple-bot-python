"""Design service responses."""
from .common import NAVIGATION, SCHEDULING

INITIAL = {
    'header': 'שירות עיצוב הבית',
    'welcome': 'אשמח לעזור לך לעצב את הבית! איזה סוג של פרויקט מעניין אותך?',
    'footer': 'יחד ניצור את הבית שתמיד חלמתם עליו!',
    'options': {
        'title': 'בחר/י מהאפשרויות:',
        'buttons': [
            'עיצוב דירה שלמה',
            'עיצוב חדר ספציפי',
            'ייעוץ צבע וטקסטיל',
            'סטיילינג ואבזור',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

STYLE_PREFERENCE = {
    'question': 'איזה סגנון עיצובי מדבר אליך?',
    'options': {
        'title': 'בחר/י:',
        'buttons': [
            'מודרני ונקי',
            'חמים וביתי',
            'סקנדינבי',
            'אקלקטי',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

BUDGET = {
    'question': 'מה התקציב המשוער שהיית רוצה להשקיע בפרויקט?',
    'options': {
        'title': 'טווח תקציב:',
        'buttons': [
            'עד 5,000 ₪',
            '5,000-15,000 ₪',
            '15,000-30,000 ₪',
            'מעל 30,000 ₪',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

COMPLETION = {
    'header': 'תודה על השיתוף!',
    'final': 'כדי שאוכל להבין טוב יותר את הצרכים והחלל, אשמח להיפגש לפגישת ייעוץ ראשונית. בפגישה נוכל לדבר על הרעיונות שלך ואוכל להציע כיווני עיצוב מתאימים.',
    'footer': 'בדרך לעיצוב המושלם!',
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
    'awaiting_style_preference': STYLE_PREFERENCE,
    'awaiting_budget': BUDGET,
    'completed': COMPLETION
}