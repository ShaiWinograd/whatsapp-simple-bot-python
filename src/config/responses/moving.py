"""Moving service responses."""
from .common import NAVIGATION, SCHEDULING

INITIAL = {
    'header': 'מעבר דירה',
    'body': "נשמח ללוות אתכם במעבר הדירה הקרוב!\nבאיזה שירות תרצו להתמקד?",
    'footer': '',
    'buttons': [
        'אריזת הבית',
        'סידור בבית החדש',
        'ליווי מלא - אריזה וסידור',
        NAVIGATION['back_to_main'],
        NAVIGATION['talk_to_representative']
    ]
}

DETAILS_TEMPLATE = """כדי שנוכל לנוודא שאנחנו זמינים בתאריך המעבר ושהכתובת שלכם נמצאת בטווח השירות שלנו.
אנא אנא שלחו בהודעה חוזרת את כל הפרטים הבאים:

שם מלא
{address_type}
כתובת מייל
תאריך הובלה מתוכנן

אם טרם נקבע תאריך הובלה, ציינו תאריך משוער"""

DETAILS_COLLECTION = {
    'packing_only': {
        'header': 'אריזה',
        'body': DETAILS_TEMPLATE.format(
            address_type='כתובת נוכחית (כולל עיר, רחוב ומספר בית)',
        ),
        'footer': '',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    },
    'unpacking_only': {
        'header': 'סידור אחרי המעבר',
        'body': DETAILS_TEMPLATE.format(
            address_type='כתובת חדשה (כולל עיר, רחוב ומספר בית)',
        ),
        'footer': '',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    },
    'both': {
        'header': 'אריזה וסידור',
        'body': DETAILS_TEMPLATE.format(
            address_type='כתובת נוכחית וחדשה (כולל עיר, רחוב ומספר בית)',
        ),
        'footer': '',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

VERIFY_DETAILS = {
    'message': """אלו הפרטים שקיבלנו ממך:

{details}

האם הפרטים נכונים?""",
    'options': {
        'buttons': [
            'כן, הפרטים נכונים',
            'לא, צריך לתקן',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

PHOTO_REQUIREMENT = {
    'message': """כדי לעזור להעריך את היקף העבודה בצורה כמה שיותר מדוייקת, נשמח לקבל תמונות או סרטון קצר של הבית:

בבקשה שימו דגש על צילום ארונות (בגדים, מטבח ואחסון) עם דלתות פתוחות

התמונות משמשות למתן הצעת המחיר בלבד ואינן נשמרות.""",
    'options': {
        'title': 'בחר/י אפשרות:',
        'buttons': [
            'מעדיפים לדלג',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

COMPLETION = {
    'after_media': """כדי להשלים את התהליך, נשמח לקיים שיחה קצרה לתיאום ציפיות.
    כדי שנדע מתי להתקשר אליכם, אנא בחרו מועד נוח מהאפשרויות הבאות:""",
}

SERVICE = {
    'name': 'מעבר דירה'
}

VERIFY = {
    'header': 'אימות פרטים',
    'footer': ''
}

PHOTOS = {
    'header': 'שליחת תמונות',
    'footer': ''
}

SCHEDULING = {
    'header': 'תיאום שיחת טלפון',
    'footer': ''
}

FALLBACK = {
    'header': 'הפניה התקבלה',
    'body': 'תודה על פנייתך! נציג מהצוות שלנו יצור איתך קשר בהקדם.',
    'footer': ''
}

REWRITE_DETAILS = {
    'header': 'עדכון פרטים',
    'body': DETAILS_TEMPLATE,  # This will be formatted with address_type in the service
    'footer': '',
    'buttons': [
        NAVIGATION['back_to_main'],
        NAVIGATION['talk_to_representative']
    ]
}

# Export all responses
RESPONSES = {
    'initial': INITIAL,
    'details_collection': DETAILS_COLLECTION,
    'verify_details': VERIFY_DETAILS,
    'photo_requirement': PHOTO_REQUIREMENT,
    'completed': COMPLETION,
    'verify': VERIFY,
    'photos': PHOTOS,
    'scheduling': SCHEDULING,
    'fallback': FALLBACK,
    'rewrite_details': REWRITE_DETAILS,
    'service_name': SERVICE['name']
}