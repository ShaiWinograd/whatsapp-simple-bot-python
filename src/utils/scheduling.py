"""Utility functions for scheduling."""
from datetime import datetime, timedelta
from typing import List, Dict

def get_available_slots(current_time: datetime = None) -> List[Dict[str, str]]:
    """
    Get the next 5 available slots for scheduling, considering working days and hours.
    
    Working hours:
    - Sunday, Tuesday, Wednesday: 10:00-12:00
    - Monday, Thursday: 17:00-19:00
    - Friday, Saturday: Closed
    
    Returns:
        List of dicts with date and time slot information
    """
    if current_time is None:
        current_time = datetime.now()
    
    # Map days to their available hours (0 = Monday)
    availability = {
        6: "10:00-12:00",  # Sunday
        0: "17:00-19:00",  # Monday
        1: "10:00-12:00",  # Tuesday
        2: "10:00-12:00",  # Wednesday
        3: "17:00-19:00",  # Thursday
        4: None,           # Friday
        5: None,           # Saturday
    }
    
    # Hebrew day names
    day_names = {
        6: "ראשון",    # Sunday
        0: "שני",      # Monday
        1: "שלישי",    # Tuesday
        2: "רביעי",    # Wednesday
        3: "חמישי",    # Thursday
        4: "שישי",     # Friday
        5: "שבת"       # Saturday
    }
    
    # Hebrew month names
    month_names = {
        1: "ינואר",
        2: "פברואר",
        3: "מרץ",
        4: "אפריל",
        5: "מאי",
        6: "יוני",
        7: "יולי",
        8: "אוגוסט",
        9: "ספטמבר",
        10: "אוקטובר",
        11: "נובמבר",
        12: "דצמבר"
    }
    
    available_slots = []
    date = current_time
    
    while len(available_slots) < 5:
        weekday = date.weekday()  # Get day of week (0 = Monday)
        # Convert to Sunday = 6, Monday = 0, etc.
        adjusted_weekday = 6 if weekday == 6 else weekday
        
        if availability[adjusted_weekday]:
            time_range = availability[adjusted_weekday]
            slot = {
                "id": str(len(available_slots)),
                "title": f"{day_names[adjusted_weekday]}, {date.day}.{month_names[date.month]} בין {time_range}"
            }
            available_slots.append(slot)
        
        date += timedelta(days=1)
    
    return available_slots