# Business Logic Module

This module contains the core business logic, flows, and message templates for the WhatsApp bot application.

## Structure

```
business/
├── __init__.py
├── messages.py         # Shared message templates and utilities
├── flow_factory.py     # Flow creation and routing
├── utils/             # Utility modules
└── flows/             # Business flow implementations
    ├── abstract_business_flow.py
    ├── moving_flow.py
    └── moving/        # Moving service specific components
        └── messages/  # Moving service message templates
            ├── __init__.py
            ├── types.py       # Type definitions
            └── responses.py   # Response templates
```

## Message Templates

Message templates are organized by service and kept close to their implementing flows:

1. Shared Components (`messages.py`):
   - Navigation options
   - Error messages
   - Common templates
   - Time slots
   - Media request templates

2. Service-Specific Messages:
   - Located in `flows/<service>/messages/`
   - Use shared components from `messages.py`
   - Include service-specific types and responses
   - Provide type-safe message structures

## Usage

### Using Shared Templates

```python
from business.messages import (
    NAVIGATION,
    create_details_message,
    MEDIA_REQUEST_TEMPLATE
)

my_message = {
    'header': 'Title',
    'body': 'Content',
    'buttons': [
        'Option 1',
        NAVIGATION['back_to_main']
    ]
}
```

### Service-Specific Messages

```python
from business.flows.moving.messages import RESPONSES

# Access moving service responses
initial_message = RESPONSES['initial']
details_form = RESPONSES['details_collection']['packing_only']
```

## Adding New Services

1. Create a new directory under `flows/` for your service
2. Add a `messages/` directory with:
   - `types.py` for type definitions
   - `responses.py` for service-specific templates
   - `__init__.py` to export responses
3. Use shared components from `messages.py`
4. Implement the service flow using the templates

## Best Practices

1. Keep message templates close to their usage in flows
2. Use type hints for better code safety
3. Leverage shared components to maintain consistency
4. Document message structures and purpose
5. Group related messages by service
6. Use environment variables for configurable values
7. Keep messages in their original language (Hebrew)