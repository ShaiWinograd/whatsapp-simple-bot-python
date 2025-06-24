# WhatsApp Simple Bot Python

A modular WhatsApp bot built with Python, using the WhatsApp Cloud API. The bot provides moving and organization services through a conversational interface, with more services planned for future implementation.

## Project Structure

```
whatsapp-simple-bot-python/
├── tests/                  # Test suite
│   ├── __init__.py
│   ├── conftest.py        # Common test fixtures
│   └── services/          # Service tests
│       ├── test_base_service.py
│       ├── test_moving_service.py
│       └── test_organization_service.py
├── src/                    # Source code
│   ├── chat/              # Chat handling
│   │   ├── __init__.py
│   │   ├── conversation_manager.py  # Manages chat state
│   │   └── message_handler.py       # Message processing
│   ├── config/            # Configuration files
│   │   ├── __init__.py
│   │   └── responses/     # Message responses
│   │       ├── moving.py
│   │       ├── common.py
│   │       └── organization.py
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   └── webhook_payload.py  # Webhook payload models
│   ├── services/          # Business logic services
│   │   ├── __init__.py
│   │   ├── base_service.py
│   │   ├── moving_service.py
│   │   ├── organization_service.py
│   │   └── service_factory.py
│   ├── utils/             # Utility functions
│   │   ├── __init__.py
│   │   ├── container.py   # Dependency container
│   │   ├── errors.py      # Error handling
│   │   ├── validators.py  # Message validation
│   │   └── whatsapp_client.py  # WhatsApp API client
│   └── __init__.py
├── assets/                # Media assets
│   └── media/            
├── docs/                  # Documentation
│   └── moving_service_flow.md  # Moving service documentation
├── app.py                 # Flask application entry point
├── requirements.txt       # Project dependencies
└── .env.template          # Environment variables template
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your configuration:
```env
TOKEN=your_whatsapp_token_here
API_URL=https://gate.whapi.cloud/
PORT=8080
```

3. Run the application:
```bash
python app.py
```

The bot will start running on `http://localhost:8080`.

## Testing

### Running Tests

Execute the test suite with coverage reporting:
```bash
pytest
```

This will:
- Run all unit tests
- Generate a coverage report in the terminal
- Create an HTML coverage report in `htmlcov/`

### Test Coverage

The test suite covers:
- Service initialization and configuration
- Conversation state management
- Message handling and validation
- Interactive message creation
- WhatsApp client integration
- Error handling
- Service-specific flows

### Writing Tests

New tests should:
1. Use fixtures from `conftest.py` for common setup
2. Mock external dependencies (WhatsApp client, etc.)
3. Test both success and error paths
4. Verify state transitions
5. Follow existing test patterns

See `tests/README.md` for detailed testing documentation.

## Features

### Core Features
- Modular and maintainable code structure
- Conversation state management
- Configurable message responses
- Early message validation
- Robust error handling
- Media message support
- Interactive buttons and dynamic responses
- Appointment scheduling system

### Services

#### Moving Service
Complete moving assistance with the following features:
- Multiple service options:
  - Packing only
  - Unpacking only
  - Combined packing and unpacking
- Detailed information collection
- Photo/video support for accurate quotes
- Automated scheduling system
- State-based conversation flow
See `docs/moving_service_flow.md` for detailed flow documentation.

#### Organization Service
Storage and organization solutions:
- Home organization consulting
- Storage optimization
- Custom organization solutions

### Technical Features
- Service-based architecture
- State machine for conversation flows
- WhatsApp Cloud API integration
- Dependency injection for better testability
- Comprehensive error handling
- Media message processing
- Dynamic scheduling system

## Webhook Configuration

The webhook endpoint is `/hook`. When configuring your WhatsApp Cloud API webhook, use:
```
https://your-domain.com/hook
```

## Message Processing Flow

1. Webhook receives incoming message
2. Validator checks if message should be processed
3. Message handler determines the appropriate service
4. Service processes the message based on conversation state
5. Conversation manager updates chat state
6. WhatsApp client sends response back to user

### Component Responsibilities

- **Services**: Handle specific business logic and maintain conversation flow
- **Conversation Manager**: Tracks and updates chat state
- **Message Handler**: Routes messages to appropriate services
- **WhatsApp Client**: Manages API communication
- **Validators**: Ensure message integrity and authorization
- **Interactive Message Builder**: Creates dynamic button-based responses

## Documentation

- Service-specific documentation can be found in the `docs/` directory
- Each service has its own detailed flow documentation
- See `moving_service_flow.md` for the complete moving service workflow
