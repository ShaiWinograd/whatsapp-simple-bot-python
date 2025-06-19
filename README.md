# WhatsApp Simple Bot Python

A modular WhatsApp bot built with Python, using the WhatsApp Cloud API.

## Project Structure

```
whatsapp-simple-bot-python/
├── src/                    # Source code
│   ├── config/            # Configuration files
│   │   ├── __init__.py
│   │   └── responses.py   # Message responses and API config
│   ├── utils/             # Utility functions
│   │   ├── __init__.py
│   │   ├── validators.py  # Message validation
│   │   └── whatsapp_client.py  # WhatsApp API client
│   ├── __init__.py
│   └── message_handler.py # Core message processing logic
├── app.py                 # Flask application entry point
├── webhook_payload.py     # Webhook payload models
└── requirements.txt       # Project dependencies
```

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create a `.env` file with your configuration:
```env
PORT=5000
```

3. Run the application:
```bash
python app.py
```

The bot will start running on `http://localhost:5000`.

## Features

- Modular and maintainable code structure
- Early message validation to improve efficiency
- Configurable message responses
- Robust error handling
- Webhook endpoint for WhatsApp Cloud API integration

## Webhook Configuration

The webhook endpoint is `/hook`. When configuring your WhatsApp Cloud API webhook, use:
```
https://your-domain.com/hook
```

## Message Processing Flow

1. Webhook receives incoming message
2. Validator checks if message should be processed
3. Message handler determines appropriate response
4. WhatsApp client sends response back to user

Each step is handled by a dedicated module for better maintainability and testability.
