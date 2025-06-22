"""Configuration for message responses"""
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

# Load environment variables
load_dotenv()

# General responses
GENERAL_RESPONSES = {
    'welcome_message': 'כדי שנוכל לתת לכם מענה מהיר ומסודר, בבקשה בחרו את השירות בו אתם מתעניינים:',
    'options': [
        'מעבר דירה',
        'סידור וארגון',
        'עיצוב והלבשת הבית',
        'שיחת ייעוץ',
        'אחר',
        'אשמח לדבר עם נציג/ה',
    ],
    'error': 'מצטערת, לא הבנתי. האם תוכל/י לנסח מחדש?'
}

# Service-specific responses
ORGANIZATION_RESPONSES = {
    'initial': {
        'welcome': 'אשמח לעזור לך לארגן ולסדר! איזה חלל צריך עזרה?',
        'options': {
            'title': 'בחר/י מהאפשרויות:',
            'buttons': [
                'חדר שינה/ארון בגדים',
                'מטבח',
                'משרד ביתי',
                'אחר'
            ]
        }
    },
    'awaiting_pain_points': {
        'question': 'מה מפריע לך במצב הנוכחי? מה היית רוצה לשפר?'
    },
    'awaiting_timing': {
        'question': 'מתי היית רוצה להתחיל בתהליך?',
        'options': {
            'title': 'בחר/י:',
            'buttons': [
                'בשבוע הקרוב',
                'בחודש הקרוב',
                'בעתיד, רק מתעניין/ת'
            ]
        }
    },
    'completed': {
        'final': 'נשמע מעולה! אשמח להיפגש לפגישת ייעוץ ללא עלות כדי להכיר את המרחב ולהציע פתרונות מותאמים אישית. האם תרצה/י לקבוע פגישה?',
        'schedule': {
            'title': 'מתי נוח לך?',
            'buttons': ['בוקר', 'צהריים', 'ערב']
        }
    }
}

MOVING_RESPONSES = {
    'initial': {
        'welcome': "איזה יופי שאתם עוברים דירה בקרוב!",
        'options': {
            'title': 'איזה סוג עזרה את/ה צריכ/ה?',
            'buttons': [
                'אריזה',
                'פריקה',
                'גם אריזה וגם פריקה'
            ]
        }
    },
    'awaiting_move_type': {
        'question': 'האם מדובר במעבר בתוך הארץ או מעבר מחו״ל?',
        'options': {
            'title': 'אנא בחר/י:',
            'buttons': [
                'מעבר בתוך הארץ',
                'מעבר מחו״ל'
            ]
        }
    },
    'awaiting_property_size': {
        'question': 'מה גודל הדירה בערך? (במ״ר)'
    },
    'awaiting_move_date': {
        'question': 'מתי בערך מתוכנן המעבר?'
    },
    'completed': {
        'final': 'תודה על הפרטים! אשמח לקבוע פגישת ייעוץ כדי לדבר על התהליך בפירוט ולהבין איך אני יכולה לעזור. האם את/ה פנוי/ה לשיחה בימים הקרובים?',
        'schedule': {
            'title': 'מתי נוח לך?',
            'buttons': [
                'הבוקר',
                'אחה״צ',
                'הערב'
            ]
        }
    }
}

DESIGN_RESPONSES = {
    'initial': {
        'welcome': 'אשמח לעזור לך לעצב את הבית! איזה סוג של פרויקט מעניין אותך?',
        'options': {
            'title': 'בחר/י מהאפשרויות:',
            'buttons': [
                'עיצוב דירה שלמה',
                'עיצוב חדר ספציפי',
                'ייעוץ צבע וטקסטיל',
                'סטיילינג ואבזור'
            ]
        }
    },
    'awaiting_style_preference': {
        'question': 'איזה סגנון עיצובי מדבר אליך?',
        'options': {
            'title': 'בחר/י:',
            'buttons': [
                'מודרני ונקי',
                'חמים וביתי',
                'סקנדינבי',
                'אקלקטי'
            ]
        }
    },
    'awaiting_budget': {
        'question': 'מה התקציב המשוער שהיית רוצה להשקיע בפרויקט?',
        'options': {
            'title': 'טווח תקציב:',
            'buttons': [
                'עד 5,000 ₪',
                '5,000-15,000 ₪',
                '15,000-30,000 ₪',
                'מעל 30,000 ₪'
            ]
        }
    },
    'completed': {
        'final': 'תודה על השיתוף! כדי שאוכל להבין טוב יותר את הצרכים והחלל, אשמח להיפגש לפגישת ייעוץ ראשונית. בפגישה נוכל לדבר על הרעיונות שלך ואוכל להציע כיווני עיצוב מתאימים.',
        'schedule': {
            'title': 'מתי נוח לך להיפגש?',
            'buttons': ['בוקר', 'צהריים', 'ערב']
        }
    }
}

CONSULTATION_RESPONSES = {
    'initial': {
        'welcome': 'אשמח לקיים איתך שיחת ייעוץ! על מה היית רוצה לדבר?',
        'options': {
            'title': 'בחר/י נושא:',
            'buttons': [
                'תכנון מעבר דירה',
                'ארגון הבית',
                'עיצוב הבית',
                'אחר'
            ]
        }
    },
    'awaiting_questions': {
        'question': 'האם יש שאלות ספציפיות שהיית רוצה שנדבר עליהן בשיחה?'
    },
    'awaiting_consultation_type': {
        'question': 'איך היית מעדיף/ה לקיים את הפגישה?',
        'options': {
            'title': 'בחר/י:',
            'buttons': [
                'פגישה פרונטלית',
                'שיחת וידאו',
                'שיחת טלפון'
            ]
        }
    },
    'completed': {
        'final': 'מעולה! אשמח לקבוע איתך את שיחת הייעוץ. פגישת ייעוץ ראשונית היא ללא עלות ונמשכת כ-45 דקות.',
        'schedule': {
            'title': 'מתי נוח לך?',
            'buttons': [
                'בימי ראשון-שלישי',
                'בימי רביעי-חמישי',
                'ביום שישי'
            ]
        }
    }
}

# Other responses for non-work related inquiries
OTHER_RESPONSES = {
    'initial': {
        'welcome': 'פנייה שלא קשורה לעבודה?',
        'options': {
            'title': 'בחר/י:',
            'buttons': ['כן', 'לא']
        }
    },
    'awaiting_service': {
        'question': 'אשמח להבין במה אני יכולה לעזור:',
        'options': {
            'title': 'בחר/י:',
            'buttons': [
                'הסבר על השירות הנדרש',
                'חזרה לתפריט הראשי'
            ]
        }
    },
    'completed': {
        'no_response': 'אוקיי, מעכשיו השיחה תמשיך כרגיל',
        'schedule_callback': 'תודה על הפנייה. מתי נוח לך שאחזור אליך?'
    }
}

# Combined responses dictionary
SERVICE_RESPONSES = {
    'organization': ORGANIZATION_RESPONSES,
    'moving': MOVING_RESPONSES,
    'design': DESIGN_RESPONSES,
    'consultation': CONSULTATION_RESPONSES,
    'אחר': OTHER_RESPONSES
}

# Exported responses combining general and service responses
RESPONSES = {
    **GENERAL_RESPONSES,
    **SERVICE_RESPONSES
}

# WhatsApp API configuration
WHATSAPP_API = {
    'base_url': os.getenv('API_URL'),
    'endpoints': {
        'text': 'messages/text',
        'interactive': 'messages/interactive'
    },
    'headers': {
        'accept': 'application/json',
        'content-type': 'application/json',
        'authorization': f"Bearer {os.getenv('TOKEN')}"
    }
}

def get_api_url(message_type: str) -> str:
    """Get the appropriate API URL based on message type."""
    endpoint = WHATSAPP_API['endpoints'].get(message_type, 'text')
    return f"{WHATSAPP_API['base_url']}{endpoint}"

# Debug phone number
DEBUG_PHONE_NUMBER = "972546626125" # Only allow messages from this number