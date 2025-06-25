"""Configuration validation module."""
import logging
from typing import Dict, Any, List
import src.config.whatsapp as whatsapp  # Import the module instead of the constant

logger = logging.getLogger(__name__)

class ConfigurationError(Exception):
    """Raised when configuration validation fails."""
    pass

class ConfigValidator:
    """Validates application configuration"""
    
    @staticmethod
    def validate_labels() -> None:
        """Validate WhatsApp label configuration
        
        Raises:
            ConfigurationError: If required labels are missing or invalid
        """
        required_labels = [
            'bot_new_conversation',
            'waiting_urgent_support',
            'waiting_call_before_quote',
            'moving',
            'organization'
        ]
        
        # Check all required labels exist
        missing_labels = [
            label for label in required_labels
            if label not in whatsapp.LABELS  # Access through module
        ]
        if missing_labels:
            logger.error(f"Missing required labels: {', '.join(missing_labels)}")
            raise ConfigurationError(f"Missing required label(s): {', '.join(missing_labels)}")
                
        # Validate label IDs are not empty
        empty_labels = [
            label for label, id_value in whatsapp.LABELS.items()  # Access through module
            if not id_value or not isinstance(id_value, str)
        ]
        if empty_labels:
            logger.error(f"Labels with invalid/empty IDs: {', '.join(empty_labels)}")
            raise ConfigurationError(
                f"Following labels have invalid/empty IDs: {', '.join(empty_labels)}"
            )
            
    @staticmethod
    def validate_responses(responses: Dict[str, Any], required_fields: List[str]) -> None:
        """Validate response message configuration
        
        Args:
            responses: Response message dictionary to validate
            required_fields: List of required field names
            
        Raises:
            ConfigurationError: If required fields are missing or invalid
        """
        # Check all required fields exist
        missing_fields = [
            field for field in required_fields
            if field not in responses
        ]
        if missing_fields:
            logger.error(f"Missing response fields: {', '.join(missing_fields)}")
            raise ConfigurationError(
                f"Missing required response fields: {', '.join(missing_fields)}"
            )
            
        # Validate field values
        invalid_fields = [
            field for field in required_fields
            if not responses[field] or not isinstance(responses[field], (str, dict, list))
        ]
        if invalid_fields:
            logger.error(f"Invalid response fields: {', '.join(invalid_fields)}")
            raise ConfigurationError(
                f"Invalid values for response fields: {', '.join(invalid_fields)}"
            )
            
    @staticmethod
    def validate_timeouts(timeout_minutes: int) -> None:
        """Validate timeout configuration
        
        Args:
            timeout_minutes: Timeout duration in minutes
            
        Raises:
            ConfigurationError: If timeout value is invalid
        """
        min_timeout = 5  # 5 minutes minimum
        max_timeout = 24 * 60  # 24 hours maximum
        
        if not isinstance(timeout_minutes, int):
            logger.error("Timeout must be an integer value")
            raise ConfigurationError("Timeout must be an integer value")
            
        if timeout_minutes < min_timeout:
            logger.error(f"Timeout {timeout_minutes} minutes is less than minimum {min_timeout}")
            raise ConfigurationError(
                f"Timeout {timeout_minutes} minutes is less than minimum {min_timeout}"
            )
            
        if timeout_minutes > max_timeout:
            logger.error(f"Timeout {timeout_minutes} minutes exceeds maximum {max_timeout}")
            raise ConfigurationError(
                f"Timeout {timeout_minutes} minutes exceeds maximum {max_timeout}"
            )
            
    @staticmethod
    def validate_all() -> None:
        """Validate all configuration settings
        
        Raises:
            ConfigurationError: If any validation fails
        """
        try:
            # Validate WhatsApp labels
            ConfigValidator.validate_labels()
            
            # Validate response messages
            from ..business.flows.moving.messages import RESPONSES
            required_fields = [
                'initial', 'details_collection', 'verify_details',
                'photo_requirement', 'completed', 'verify', 'photos',
                'scheduling', 'fallback', 'rewrite_details',
                'emergency_support', 'time_slots', 'selected_slot',
                'urgent_support_message', 'service_name'
            ]
            ConfigValidator.validate_responses(RESPONSES, required_fields)
            
            # Validate timeout (default 300 minutes = 5 hours)
            ConfigValidator.validate_timeouts(300)
            
            logger.info("All configuration validated successfully")
        except ConfigurationError as e:
            logger.error("Configuration validation failed")
            raise ConfigurationError(f"Configuration validation failed: {str(e)}")