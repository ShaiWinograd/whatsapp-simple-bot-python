"""Common response structures and general messages."""

GENERAL = {
    'intro': 'שלום!\nהגעתם לעוזר הדיגיטלי של S&O.\nאני כאן לעזור לכם למצוא את השירות המתאים ולענות על כל שאלה.\nלנוחותכם, בכל שלב ניתן לחזור לתפריט הראשי או לשוחח עם נציג/ה באמצעות הכפתורים בתחתית.',
    'header': 'ברוכים הבאים לSpace & Order',
    'welcome_message': 'בתור התחלה, אנא בחרו את השירות בו אתם מתעניינים:',
    'footer': '',
    'options': [
        'מעבר דירה',
        'סידור וארגון הבית',
        'אחר',
        'שיחה עם נציג/ה'
    ],
    'error': 'מצטערים, לא הצלחנו להבין את ההודעה. האם תוכל/י לנסח אותה מחדש?'
}

HUMAN_SUPPORT = {
    'transfer_message': 'תודה על פנייתך! נציג/ה מהצוות שלנו יחזור אליך בהקדם.'
}

SCHEDULING = {
    'header': 'תיאום פגישה',
    'title': 'איזה מועד נוח לך?',
    'footer': '',
}

NAVIGATION = {
    'back_to_main': 'חזרה לתפריט הראשי',
    'talk_to_representative': 'שיחה עם נציג/ה'
}

CALL_SCHEDULING = {
    'confirmation': {
        'header': 'תיאום שיחה',
        'body_template': 'מעולה! נציג שלנו יתקשר אליך ב{slot}.',
        'footer': 'אם תרצו לשנות את מועד השיחה, לחצו על הכפתור למטה',
        'change_slot_button': 'שינוי מועד השיחה'
    }
}