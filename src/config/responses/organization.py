"""Organization service responses."""
from .common import NAVIGATION, SCHEDULING

DETAILS = """כדי שנוכל לוודא שאתם גרים בטווח השירות שלנו, אנא שלחו בהודעה חוזרת את כל הפרטים הבאים:

שם מלא
כתובת (עיר, רחוב ומספר בית)
כתובת מייל
ספרו בקצרה על ההרכב המשפחתי ואופי הסידור המבוקש:
כל הבית, חדר מסוים, שינוי בין חדרים, הוספת פתרונות אחסון וכו׳
"""

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

REWRITE_DETAILS = {
    'header': 'ארגון וסידור הבית',
    'body': DETAILS,
    'footer': '',
    'buttons': [
        NAVIGATION['back_to_main'],
        NAVIGATION['talk_to_representative']
    ]
}

COMPLETION = {
    'header': 'מוכנים להתחיל?',
    'after_media': """נהדר! הצעד הראשון הוא פגישת ייעוץ חינמית בה נכיר את המרחב שלך ונבנה יחד תכנית פעולה מותאמת אישית.
כדי שנדע מתי להתקשר אליכם, אנא בחרו מועד נוח מהאפשרויות הבאות:""",
    'footer': ''
}

SERVICE = {
    'name': 'ארגון וסידור הבית'
}

VERIFY = {
    'header': 'אימות פרטים',
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

# Export all responses
RESPONSES = {
    'initial': DETAILS,
    'verify_details': VERIFY_DETAILS,
    'completed': COMPLETION,
    'verify': VERIFY,
    'scheduling': SCHEDULING,
    'fallback': FALLBACK,
    'rewrite_details': REWRITE_DETAILS,
    'service_name': SERVICE['name']
}