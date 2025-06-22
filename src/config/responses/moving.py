"""Moving service responses."""
from .common import NAVIGATION, SCHEDULING

INITIAL = {
    'header': '🏠 מעבר דירה',
    'welcome': "איזה יופי שאתם עוברים דירה בקרוב! ✨",
    'footer': 'אנחנו כאן ללוות אתכם בכל שלב 🏡',
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
        'header': 'שירות אריזה 📦',
        'body': PRICE_QUOTE_BASE.format(
            address_type='כתובת של הבית הנוכחי',
            extra_fields=''
        ),
        'footer': 'מחכים לעזור לכם לארוז! 🏡',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    },
    'unpacking_only': {
        'header': 'שירות סידור וארגון אחרי מעבר 🏠',
        'body': PRICE_QUOTE_BASE.format(
            address_type='כתובת של הבית החדש',
            extra_fields=''
        ),
        'footer': 'נעזור לכם להרגיש בבית! 🏡',
        'buttons': [
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    },
    'both': {
        'header': 'שירות אריזה ופריקה 🏠📦',
        'body': PRICE_QUOTE_BASE.format(
            address_type='כתובת של הבית הנוכחי',
            extra_fields='3. כתובת של הבית החדש\n'
        ),
        'footer': 'נלווה אתכם לאורך כל הדרך! 🏡✨',
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
        'title': 'הפרטים נכונים?',
        'buttons': [
            '✅ כן, הפרטים נכונים',
            '❌ לא, צריך לתקן',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

PHOTO_REQUIREMENT = {
    'message': """כדי שנוכל להעריך את היקף העבודה, נשמח לקבל תמונות או סרטון של רהיטי האחסון בבית (ארונות, שידות וכו׳) כשהדלתות והמגירות פתוחות.
אנחנו לא שופטים ואין לנו ציפייה למצב מסוים - ראינו הכל! המטרה היא רק להעריך את היקף העבודה ולתת הצעת מחיר מדויקת."""
}

MOVE_TYPE = {
    'question': '🌍 האם מדובר במעבר בתוך הארץ או מעבר מחו״ל?',
    'options': {
        'title': 'אנא בחר/י:',
        'buttons': [
            '🚚 מעבר בתוך הארץ',
            '✈️ מעבר מחו״ל',
            NAVIGATION['talk_to_representative']
        ]
    }
}

PROPERTY_SIZE = {
    'question': '🏠 מה גודל הדירה בערך? (במ״ר)'
}

MOVE_DATE = {
    'question': '📅 מתי בערך מתוכנן המעבר?'
}

COMPLETION = {
    'header': '✨ תודה על השיתוף! ✨',
    'final': 'אשמח לקבוע פגישת ייעוץ כדי לדבר על התהליך בפירוט ולהבין איך אני יכולה לעזור. האם את/ה פנוי/ה לשיחה בימים הקרובים?',
    'footer': 'בדרך לבית החדש שלכם! 🏡',
    'schedule': {
        **SCHEDULING,
        'buttons': [
            '🌅 הבוקר',
            '☀️ אחה״צ',
            '🌙 הערב',
            NAVIGATION['talk_to_representative']
        ]
    }
}

# Export all responses
RESPONSES = {
    'initial': INITIAL,
    'price_quote': PRICE_QUOTE,
    'verify_details': VERIFY_DETAILS,
    'photo_requirement': PHOTO_REQUIREMENT,
    'awaiting_move_type': MOVE_TYPE,
    'awaiting_property_size': PROPERTY_SIZE,
    'awaiting_move_date': MOVE_DATE,
    'completed': COMPLETION
}