# Configuration Module

This module handles all configuration settings and response templates for the WhatsApp bot application.

## Structure

```
config/
├── __init__.py         # Environment validation and initialization
├── debug.py           # Debug and development settings
├── whatsapp.py        # WhatsApp API configuration
├── README.md          # This file
└── responses/         # Message templates and responses
    ├── __init__.py
    ├── types.py       # Type definitions for responses
    ├── templates.py   # Shared message templates
    ├── common.py      # Common responses and navigation
    ├── moving.py      # Moving service responses
    ├── organization.py # Organization service responses
    └── other service responses...
```

## Usage

### Environment Variables

Required environment variables are validated on module import. Copy `.env.template` to `.env` and set the following variables:

```
API_URL=                    # WhatsApp API base URL
TOKEN=                      # WhatsApp API authorization token
WHATSAPP_*_LABEL_ID=       # Various WhatsApp label IDs
DEBUG_PHONE_NUMBER=         # (Optional) Restrict messages to this number in dev mode
DEV_MODE=                  # (Optional) Enable development mode features
```

### Adding New Responses

1. Define type structures in `responses/types.py`
2. Add shared templates to `responses/templates.py` if needed
3. Create service-specific responses using the defined types
4. Export responses through a typed RESPONSES dictionary

Example:
```python
from .types import ButtonMessage, ResponseCollection
from .templates import create_details_message

MY_MESSAGE: ButtonMessage = {
    'header': 'Title',
    'body': 'Content',
    'footer': '',
    'buttons': ['Option 1', 'Option 2']
}

RESPONSES: ResponseCollection = {
    'my_message': MY_MESSAGE,
    ...
}
```

### Best Practices

1. Always use type hints defined in `types.py`
2. Extract shared templates to avoid duplication
3. Use environment variables for configurable values
4. Document message structures and usage
5. Group related messages in service-specific files
6. Use the `NAVIGATION` constants for consistent buttons
7. Keep messages in their original language (Hebrew)

## Contributing

When adding or modifying configuration:

1. Update environment variables in `.env.template`
2. Add type definitions for new structures
3. Document changes in relevant README files
4. Use existing templates where possible
5. Follow the established file organization
6. Ensure all strings are properly localized
7. Add validation for required settings

## Testing

Configuration validation occurs on module import. Run the application's test suite to verify your changes:

```bash
pytest tests/config/