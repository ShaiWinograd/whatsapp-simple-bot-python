"""Configuration module for the application.

This module initializes and validates all configuration settings including:
- Environment variables
- API configurations
- Debug settings
"""
from typing import List, Tuple
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def _get_env_vars() -> Tuple[List[str], List[str]]:
    """Get lists of required and optional environment variables.
    
    Returns:
        Tuple of (required vars, optional vars)
    """
    required = [
        'API_URL',
        'TOKEN',
        'WHATSAPP_BOT_NEW_CONVERSATION_LABEL_ID',
        'WHATSAPP_URGENT_SUPPORT_LABEL_ID',
        'WHATSAPP_WAITING_CALL_BEFORE_QUOTE_LABEL_ID',
        'WHATSAPP_MOVING_LABEL_ID',
        'WHATSAPP_ORGANIZATION_LABEL_ID',
    ]
    
    optional = [
        'DEBUG_PHONE_NUMBER',  # Only needed in development
        'DEV_MODE'            # Enable development features
    ]
    
    return required, optional

def validate_env_vars() -> None:
    """Validate that all required environment variables are set.
    
    Optional variables are allowed to be missing.
    
    Raises:
        EnvironmentError: If any required variables are missing
    """
    required_vars, _ = _get_env_vars()
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    if missing_vars:
        raise EnvironmentError(
            f"Missing required environment variables: {', '.join(missing_vars)}"
        )

# Validate environment variables on module import
validate_env_vars()