# WhatsApp Simple Bot Python

A modular WhatsApp bot built with Python, using the WhatsApp Cloud API. The bot provides moving and organization services through a conversational interface, with more services planned for future implementation.

## Project Structure

```
whatsapp-simple-bot-python/
├── src/                    # Source code
│   ├── chat/              # Chat handling
│   │   ├── __init__.py
│   │   ├── conversation_manager.py  # Manages chat state
│   │   └── message_handler.py       # Message processing
│   ├── config/            # Configuration files
│   │   ├── __init__.py
│   │   └── responses.py   # Message responses and API config
│   ├── models/            # Data models
│   │   ├── __init__.py
│   │   └── webhook_payload.py  # Webhook payload models
│   ├── services/          # Business logic services
│   │   ├── __init__.py
│   │   ├── base_service.py
│   │   ├── moving_service.py
│   │   ├── organization_service.py
│   │   ├── other_service.py
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

## Features

- Modular and maintainable code structure
- Service-based architecture for business functions:
  - Moving service: Handles moving-related inquiries and bookings
  - Organization service: Manages organization and storage solutions
  - Additional services planned for future implementation
- Conversation state management
- Configurable message responses
- Early message validation to improve efficiency
- Robust error handling
- Webhook endpoint for WhatsApp Cloud API integration
- Dependency injection for better testability
- Media message support

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

Each component is designed to be modular and maintainable, with clear separation of concerns:
- Services handle specific business logic
- Conversation manager tracks chat state
- Message handler routes messages to appropriate services
- WhatsApp client handles API communication
