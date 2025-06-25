"""Utility functions for scheduling."""
from datetime import datetime, timedelta
from typing import List, Dict
from src.utils.logger import setup_logger
from .localization import format_date_hebrew

logger = setup_logger(__name__)

def get_available_slots(current_time: datetime = None) -> List[Dict[str, str]]:
    """
    Get the next 5 available slots for scheduling, considering working days and hours.
    
    Working hours:
    - Sunday, Tuesday, Wednesday: 10:00-12:00
    - Monday, Thursday: 17:00-19:00
    - Friday, Saturday: Closed
    
    Args:
        current_time (datetime, optional): Override current time for testing
    
    Returns:
        List[Dict[str, str]]: List of dicts with date and time slot information
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
    
    available_slots = []
    # Start from tomorrow
    date = current_time + timedelta(days=1)
    logger.debug("Starting slot calculation from date %s (tomorrow)", date)
    
    while len(available_slots) < 5:
        weekday = date.weekday()  # Get day of week (0 = Monday)
        time_range = availability[weekday]
        
        if time_range:
            slot = {
                "id": str(len(available_slots)),
                "title": format_date_hebrew(date.day, date.month, time_range)
            }
            logger.debug("Created slot: %s", slot)
            available_slots.append(slot)
        else:
            logger.debug("No availability for weekday %d", weekday)
        
        date += timedelta(days=1)
    
    logger.debug("Generated %d available slots", len(available_slots))
    return available_slots