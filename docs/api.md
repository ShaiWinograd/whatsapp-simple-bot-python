# WhatsApp Bot API Documentation

## Overview

This API provides WhatsApp messaging functionality for the moving service bot. It handles message processing, state management, and business flow coordination.

## Endpoints

### POST /webhook

Handles incoming WhatsApp messages and events.

#### Request
```json
{
    "object": "whatsapp_business_account",
    "entry": [{
        "id": "WHATSAPP_BUSINESS_ACCOUNT_ID",
        "changes": [{
            "value": {
                "messaging_product": "whatsapp",
                "metadata": {
                    "display_phone_number": "PHONE_NUMBER",
                    "phone_number_id": "PHONE_NUMBER_ID"
                },
                "contacts": [{
                    "profile": {
                        "name": "USER_NAME"
                    },
                    "wa_id": "USER_PHONE_NUMBER"
                }],
                "messages": [{
                    "from": "USER_PHONE_NUMBER",
                    "id": "MESSAGE_ID",
                    "timestamp": "TIMESTAMP",
                    "type": "text",
                    "text": {
                        "body": "MESSAGE_CONTENT"
                    }
                }]
            },
            "field": "messages"
        }]
    }]
}
```

#### Response
```json
{
    "success": true
}
```

### GET /health

Health check endpoint.

#### Response
```json
{
    "status": "healthy",
    "version": "1.0.0",
    "uptime": "10h 30m"
}
```

## Message Types

### Text Message
```json
{
    "type": "text",
    "text": {
        "body": "Message content"
    }
}
```

### Interactive Message
```json
{
    "type": "interactive",
    "interactive": {
        "type": "button",
        "header": {
            "type": "text",
            "text": "Header text"
        },
        "body": {
            "text": "Body text"
        },
        "footer": {
            "text": "Footer text"
        },
        "action": {
            "buttons": [
                {
                    "type": "reply",
                    "reply": {
                        "id": "button_id",
                        "title": "Button text"
                    }
                }
            ]
        }
    }
}
```

### Media Message
```json
{
    "type": "image",
    "image": {
        "id": "IMAGE_ID",
        "mime_type": "image/jpeg",
        "sha256": "IMAGE_HASH",
        "caption": "Optional caption"
    }
}
```

## Flow States

The API manages these conversation states:

- `initial`: Initial service selection
- `awaiting_packing_choice`: Service type selection
- `awaiting_customer_details`: Address collection
- `awaiting_verification`: Details verification
- `awaiting_photos`: Photo submission
- `awaiting_emergency_support`: Support handling
- `awaiting_slot_selection`: Time slot selection
- `awaiting_reschedule`: Reschedule handling
- `completed`: Flow completion

## Labels

The API manages these conversation labels:

- `bot_new_conversation`: New conversations
- `moving`: Moving service conversations
- `waiting_urgent_support`: Urgent support requests
- `waiting_call_before_quote`: Completed conversations

## Error Responses

### 400 Bad Request
```json
{
    "error": "Invalid message format",
    "details": "Missing required field: type"
}
```

### 401 Unauthorized
```json
{
    "error": "Invalid authentication",
    "details": "Missing or invalid token"
}
```

### 429 Too Many Requests
```json
{
    "error": "Rate limit exceeded",
    "details": "Too many requests",
    "retry_after": 60
}
```

### 500 Internal Server Error
```json
{
    "error": "Internal server error",
    "request_id": "unique_request_id"
}
```

## Rate Limits

- Maximum 20 requests per second per user
- Maximum 1000 requests per hour per user
- Maximum 10000 requests per day per user

## Authentication

The API requires a WhatsApp Business API token for authentication:

```http
Authorization: Bearer YOUR_TOKEN
```

## Webhooks

Configure your webhook URL in the WhatsApp Business API dashboard:

1. Go to Business Settings > API Setup
2. Enter your webhook URL
3. Verify your webhook
4. Select subscribed fields:
   - messages
   - message_status
   - conversations