"""Moving service responses."""
from .common import NAVIGATION, SCHEDULING

INITIAL = {
    'header': 'מעבר דירה 🏠',
    'welcome': "איזה יופי שאתם עוברים דירה בקרוב ✨! באיזה שירות אתם מעוניינים?",
    'footer': '',
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

PRICE_QUOTE_BASE = """ בבקשה שלחו הודעה מסודרת הכוללת את כל הפרטים הבאים:

- שם מלא
- {address_type}
{extra_fields}- מייל
- תאריך הובלה.
במידה ואין תאריך הובלה, ציינו את תאריך המעבר המשוער."""

PRICE_QUOTE = {
    'packing_only': {
        'header': 'אריזה 📦',
        'body': PRICE_QUOTE_BASE.format(
            address_type='כתובת נוכחית (כולל עיר, רחוב ומספר בית)',
            extra_fields=''
        ),
        'footer': '',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    },
    'unpacking_only': {
        'header': 'סידור אחרי מעבר 🏠',
        'body': PRICE_QUOTE_BASE.format(
            address_type='כתובת חדשה (כולל עיר, רחוב ומספר בית)',
            extra_fields=''
        ),
        'footer': '',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    },
    'both': {
        'header': 'אריזה ופריקה 📦🏠',
        'body': PRICE_QUOTE_BASE.format(
            address_type='כתובת נוכחית (כולל עיר, רחוב ומספר בית)',
            extra_fields='- כתובת חדשה (כולל עיר, רחוב ומספר בית)\n'
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
    'message': """על מנת שנוכל לשלוח הצעת מחיר מדוייקת נשמח לקבל סרטון או תמונות של תכולת הבית הנוכחי. את כל הארונות (בגדים, מטבח או אחסון כללי) צלמו עם הדלתות פתוחות. התמונות עוזרות להעריך את היקף העבודה ולא נועדו לאף מטרה אחרת.""",
    'options': {
        'title': 'בחר/י אפשרות:',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

COMPLETION = {
    'after_media': """כדי להשלים את תהליך קבלת הצעת המחיר, נצטרך לקיים שיחת טלפון קצרה עם אחד מנציגי התמיכה שלנו."
            "\n\nנציגינו זמינים בימים ראשון עד חמישי בשעות הבאות:"
            "\nימים ראשון, שלישי ורביעי: 10:00-12:00"
            "\nימים שני וחמישי: 17:00-19:00"
            "\n\nאנא בחר/י מועד מתאים מהאפשרויות הבאות:"""
}

# Export all responses
RESPONSES = {
    'initial': INITIAL,
    'price_quote': PRICE_QUOTE,
    'verify_details': VERIFY_DETAILS,
    'photo_requirement': PHOTO_REQUIREMENT,
    'completed': COMPLETION
}