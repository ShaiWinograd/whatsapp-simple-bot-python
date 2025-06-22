"""Moving service responses."""
from .common import NAVIGATION, SCHEDULING

INITIAL = {
    'header': 'מעבר דירה 🏠',
    'welcome': "איזה יופי שאתם עוברים דירה בקרוב ✨! במה אנחנו יכולים לעזור?",
    'footer': 'נשמח ללוות אתכם בתהליך 🏡',
    'options': {
        'buttons': [
            'אריזה 📦',
            'סידור אחרי המעבר 🏡',
            'גם וגם ✨',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

PRICE_QUOTE_BASE = """כדי שנוכל לשלוח הצעת מחיר מדויקת, בבקשה שלחו הודעה מסודרת הכוללת את כל הפרטים הבאים:

1.⁠ ⁠שם מלא
2.⁠ ⁠{address_type}
{extra_fields}3.⁠ ⁠מייל
4.⁠ ⁠תאריך הובלה.
במידה ואין תאריך הובלה, ציינו את התאריך המשוער."""

PRICE_QUOTE = {
    'packing_only': {
        'header': 'אריזה 📦',
        'body': PRICE_QUOTE_BASE.format(
            address_type='כתובת של הבית הנוכחי',
            extra_fields=''
        ),
        'footer': 'מחכים לעזור לכם לארוז 🏡!',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    },
    'unpacking_only': {
        'header': 'סידור וארגון אחרי מעבר 🏠',
        'body': PRICE_QUOTE_BASE.format(
            address_type='כתובת של הבית החדש',
            extra_fields=''
        ),
        'footer': 'נעזור לכם להרגיש בבית 🏡!',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    },
    'both': {
        'header': 'אריזה ופריקה 📦🏠',
        'body': PRICE_QUOTE_BASE.format(
            address_type='כתובת של הבית הנוכחי',
            extra_fields='3. כתובת של הבית החדש\n'
        ),
        'footer': 'נלווה אתכם לאורך כל הדרך 🏡✨!',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

VERIFY_DETAILS = {
    'message': """זה מה שקיבלנו ממך:

{details}

האם הפרטים נכונים?""",
    'options': {
        'buttons': [
            'כן, הפרטים נכונים ✅',
            'לא, צריך לתקן ❌',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

PHOTO_REQUIREMENT = {
    'message': """כדי שנוכל להעריך את היקף העבודה ולתת הצעת מחיר מדויקת, נשמח לקבל תמונות או סרטון של רהיטי האחסון בבית (ארונות, שידות וכו׳) כשהדלתות והמגירות פתוחות.

חשוב לציין - התמונות עוזרות לנו לתת הצעת מחיר מדויקת יותר ולהיערך טוב יותר לעבודה. אנחנו לא שופטים ואין לנו ציפייה למצב מסוים - ראינו הכל!

אנא שלח/י תמונות או סרטון, או בחר/י באחת מהאפשרויות למטה:""",
    'options': {
        'title': 'בחר/י אפשרות:',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

COMPLETION = {
    'after_media': """תודה רבה על התמונות!."""
}

# Export all responses
RESPONSES = {
    'initial': INITIAL,
    'price_quote': PRICE_QUOTE,
    'verify_details': VERIFY_DETAILS,
    'photo_requirement': PHOTO_REQUIREMENT,
    'completed': COMPLETION
}