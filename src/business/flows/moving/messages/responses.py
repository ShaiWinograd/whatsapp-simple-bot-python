"""Moving service response configurations.

This module contains all message templates and configurations specific to
the moving service flow.
"""
from typing import Dict
from ....messages import (
    NAVIGATION,
    DEFAULT_TIME_SLOTS,
    MEDIA_REQUEST_TEMPLATE,
    create_details_message
)
from .types import (
    ButtonMessage,
    MessageWithOptions,
    BaseMessage,
    ServiceResponse,
    MovingResponseCollection
)

# Initial service selection
INITIAL: ButtonMessage = {
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

# Details collection for different service types
DETAILS_COLLECTION: Dict[str, ButtonMessage] = {
    'packing_only': create_details_message(
        'אריזה',
        'כתובת נוכחית (כולל עיר, רחוב ומספר בית)'
    ),
    'unpacking_only': create_details_message(
        'סידור אחרי המעבר',
        'כתובת חדשה (כולל עיר, רחוב ומספר בית)'
    ),
    'both': create_details_message(
        'אריזה וסידור',
        'כתובת נוכחית וחדשה (כולל עיר, רחוב ומספר בית)'
    )
}

# Details verification
VERIFY_DETAILS: MessageWithOptions = {
    'header': 'אימות פרטים',
    'body': """אלו הפרטים שקיבלנו ממך:

{details}

האם הפרטים נכונים?""",
    'footer': '',
    'options': {
        'title': 'האם הפרטים נכונים?',
        'buttons': [
            'כן, הפרטים נכונים',
            'לא, צריך לתקן',
            NAVIGATION['back_to_main'],
            NAVIGATION['talk_to_representative']
        ]
    }
}

# Emergency support inquiry
EMERGENCY_SUPPORT: ButtonMessage = {
    'header': 'תמיכה דחופה',
    'body': 'האם הפנייה דחופה ודורשת שיחה מנציג כמה שיותר מהר?',
    'footer': '',
    'buttons': ['כן', 'לא']
}

# Time slot selection
TIME_SLOTS: ButtonMessage = {
    'header': 'תיאום שיחה',
    'body': 'נא לבחור שעה נוחה לשיחה:',
    'footer': '',
    'buttons': [
        *DEFAULT_TIME_SLOTS.values(),
        NAVIGATION['back_to_main'],
        NAVIGATION['talk_to_representative']
    ]
}

# Selected time slot confirmation
SELECTED_SLOT: ButtonMessage = {
    'header': 'אישור תיאום',
    'body': 'נציג יצור איתך קשר {slot}\nרוצה לשנות את השעה?',
    'footer': '',
    'buttons': [
        'לקבוע זמן אחר',
        NAVIGATION['back_to_main'],
        NAVIGATION['talk_to_representative']
    ]
}

# Service completion messages
COMPLETION: Dict[str, str] = {
    'after_media': """כדי להשלים את התהליך, נשמח לקיים שיחה קצרה לתיאום ציפיות.
    כדי שנדע מתי להתקשר אליכם, אנא בחרו מועד נוח מהאפשרויות הבאות:"""
}

SERVICE: ServiceResponse = {
    'name': 'מעבר דירה'
}

# Base messages
VERIFY: BaseMessage = {
    'header': 'אימות פרטים',
    'body': '',  # Will be populated dynamically
    'footer': ''
}

PHOTOS = MEDIA_REQUEST_TEMPLATE  # Export directly for backward compatibility

SCHEDULING: BaseMessage = {
    'header': 'תיאום שיחת טלפון',
    'body': '',  # Will be populated dynamically
    'footer': ''
}

FALLBACK: BaseMessage = {
    'header': 'הפניה התקבלה',
    'body': 'תודה על פנייתך! נציג מהצוות שלנו יצור איתך קשר בהקדם.',
    'footer': ''
}

# Export all responses with type safety
RESPONSES: MovingResponseCollection = {
    'initial': INITIAL,
    'details_collection': DETAILS_COLLECTION,
    'verify_details': VERIFY_DETAILS,
    'photo_requirement': MEDIA_REQUEST_TEMPLATE,
    'completed': COMPLETION,
    'verify': VERIFY,
    'photos': MEDIA_REQUEST_TEMPLATE,
    'scheduling': SCHEDULING,
    'fallback': FALLBACK,
    'rewrite_details': DETAILS_COLLECTION['both'],  # Reuse the both template
    'emergency_support': EMERGENCY_SUPPORT,
    'time_slots': TIME_SLOTS,
    'selected_slot': SELECTED_SLOT,
    'urgent_support_message': 'פנייתך התקבלה, נציג שלנו יחזור אליך בדקות הקרובות.',
    'service_name': SERVICE['name']
}

__all__ = [
    'RESPONSES',
    'SERVICE',
    'TIME_SLOTS',
    'SELECTED_SLOT',
    'EMERGENCY_SUPPORT',
    'INITIAL',
    'DETAILS_COLLECTION',
    'VERIFY_DETAILS',
    'VERIFY',
    'PHOTOS'
]