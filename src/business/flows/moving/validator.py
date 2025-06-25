"""Validation module for moving service flow inputs."""
from typing import Dict, Any, Union
import re

class MovingFlowValidator:
    """Validator for moving flow inputs"""
    
    def __init__(self):
        self._address_pattern = re.compile(r'^[א-ת\s,0-9]+$')
        self._min_address_length = 10
        self._max_address_length = 200
        
    def validate_customer_details(self, details: str) -> bool:
        """Validate customer address details
        
        Args:
            details (str): Address details to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        if not details or not isinstance(details, str):
            return False
            
        # Clean whitespace
        details = details.strip()
        
        # Check length
        if len(details) < self._min_address_length:
            return False
            
        if len(details) > self._max_address_length:
            return False
            
        # Check format (Hebrew letters, numbers, spaces, commas)
        if not self._address_pattern.match(details):
            return False
            
        # Must contain at least one number (for house number)
        if not any(char.isdigit() for char in details):
            return False
            
        return True
        
    def validate_photo(self, photo_data: Union[str, Dict[str, Any]]) -> bool:
        """Validate photo submission
        
        Args:
            photo_data: Photo data to validate, can be media ID string or dict with metadata
            
        Returns:
            bool: True if valid, False otherwise
        """
        # For dictionary input, validate metadata
        if isinstance(photo_data, dict):
            # Check required metadata
            required_fields = ['id', 'mime_type']
            if not all(field in photo_data for field in required_fields):
                return False
                
            # Validate mime type
            valid_mime_types = ['image/jpeg', 'image/png']
            if photo_data.get('mime_type') not in valid_mime_types:
                return False
                
            # Add size validation if available
            if 'file_size' in photo_data:
                max_size = 5 * 1024 * 1024  # 5MB
                if photo_data['file_size'] > max_size:
                    return False
                    
            return True
            
        # For non-dictionary input, treat as invalid
        return False
        
    def validate_time_slot(self, time_slot: str, available_slots: Dict[str, str]) -> bool:
        """Validate selected time slot
        
        Args:
            time_slot (str): Selected time slot
            available_slots (Dict[str, str]): Available time slots
            
        Returns:
            bool: True if valid slot, False otherwise
        """
        return time_slot in available_slots.values()