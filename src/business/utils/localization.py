"""Localization utilities and string resources."""
from typing import Dict

# Hebrew day names
HEBREW_DAYS = {
    6: "ראשון",    # Sunday
    0: "שני",      # Monday
    1: "שלישי",    # Tuesday
    2: "רביעי",    # Wednesday
    3: "חמישי",    # Thursday
    4: "שישי",     # Friday
    5: "שבת"       # Saturday
}

# Hebrew month names
HEBREW_MONTHS = {
    1: "ינואר",     # January
    2: "פברואר",    # February
    3: "מרץ",       # March
    4: "אפריל",     # April
    5: "מאי",       # May
    6: "יוני",      # June
    7: "יולי",      # July
    8: "אוגוסט",    # August
    9: "ספטמבר",    # September
    10: "אוקטובר",  # October
    11: "נובמבר",   # November
    12: "דצמבר"     # December
}

def format_date_hebrew(day_num: int, month_num: int, time_range: str) -> str:
    """
    Format a date string in Hebrew.
    
    Args:
        day_num (int): Day of week (0-6, where 0 is Monday)
        month_num (int): Month number (1-12)
        time_range (str): Time range string
        
    Returns:
        str: Formatted date string in Hebrew
    """
    # Convert Monday=0 to Sunday=6 format
    adjusted_day = 6 if day_num == 6 else day_num
    
    return f"{HEBREW_DAYS[adjusted_day]}, {day_num} ב{HEBREW_MONTHS[month_num]} בין {time_range}"