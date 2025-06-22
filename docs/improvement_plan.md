# WhatsApp Bot Code Improvement Plan

## Overview

This document outlines a comprehensive plan for improving the WhatsApp bot codebase. The improvements focus on architecture, testing, performance, code quality, and documentation.

## Table of Contents
- [1. Architecture Improvements](#1-architecture-improvements)
- [2. Testing Strategy](#2-testing-strategy)
- [3. Performance Improvements](#3-performance-improvements)
- [4. Code Quality Improvements](#4-code-quality-improvements)
- [5. Documentation Improvements](#5-documentation-improvements)

## 1. Architecture Improvements

### 1.1 Service Layer Refinement

#### Current Issues:
- Global state for conversation management
- No timeout mechanism for stale conversations
- Direct service instantiation without proper factory pattern
- Lack of proper separation of concerns

#### Implementation Plan:

1. Create ConversationManager Class:
```python
from datetime import datetime, timedelta

class ConversationManager:
    def __init__(self, timeout_minutes: int = 30):
        self.conversations: Dict[str, BaseConversationService] = {}
        self.last_activity: Dict[str, datetime] = {}
        self.timeout_minutes = timeout_minutes
    
    def add_conversation(self, user_id: str, service: BaseConversationService) -> None:
        self.conversations[user_id] = service
        self.last_activity[user_id] = datetime.now()
    
    def get_conversation(self, user_id: str) -> Optional[BaseConversationService]:
        if self.is_conversation_active(user_id):
            self.last_activity[user_id] = datetime.now()
            return self.conversations.get(user_id)
        return None
    
    def cleanup_stale_conversations(self) -> None:
        current_time = datetime.now()
        stale_users = [
            user_id for user_id, last_active in self.last_activity.items()
            if (current_time - last_active) > timedelta(minutes=self.timeout_minutes)
        ]
        for user_id in stale_users:
            self.conversations.pop(user_id, None)
            self.last_activity.pop(user_id, None)
```

2. Implement Service Factory:
```python
from enum import Enum
from typing import Type, Dict

class ServiceType(Enum):
    ORGANIZATION = "organization"
    DESIGN = "design"
    CONSULTATION = "consultation"
    MOVING = "moving"

class ServiceFactory:
    _services: Dict[ServiceType, Type[BaseConversationService]] = {}
    
    @classmethod
    def register(cls, service_type: ServiceType, service_class: Type[BaseConversationService]) -> None:
        cls._services[service_type] = service_class
    
    @classmethod
    def create(cls, service_type: ServiceType, recipient: str) -> BaseConversationService:
        service_class = cls._services.get(service_type)
        if not service_class:
            raise ValueError(f"Unknown service type: {service_type}")
        return service_class(recipient)
```

### 1.2 Dependency Injection

#### Current Issues:
- Static WhatsApp client usage
- Hard-coded dependencies
- Difficult to test components in isolation

#### Implementation Plan:

1. Create Service Container:
```python
from dependency_injector import containers, providers

class Container(containers.DeclarativeContainer):
    config = providers.Configuration()
    
    # Services
    whatsapp_client = providers.Singleton(
        WhatsAppClient,
        api_url=config.whatsapp.api_url,
        headers=config.whatsapp.headers
    )
    
    conversation_manager = providers.Singleton(
        ConversationManager,
        timeout_minutes=config.conversation.timeout_minutes
    )
    
    service_factory = providers.Singleton(
        ServiceFactory
    )
```

2. Modify WhatsApp Client:
```python
class WhatsAppClient:
    def __init__(self, api_url: str, headers: dict):
        self.api_url = api_url
        self.headers = headers
        self.session = requests.Session()
    
    def send_message(self, payload: dict) -> dict:
        """Send message with proper error handling and retries"""
        try:
            response = self.session.post(
                self.api_url,
                json=payload,
                headers=self.headers
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            logger.error(f"WhatsApp API error: {e}")
            raise WhatsAppAPIError(str(e))
```

### 1.3 Configuration Management

#### Current Issues:
- Scattered configuration
- No validation of configuration values
- No environment-specific configs

#### Implementation Plan:

1. Create Configuration Classes:
```python
from pydantic import BaseSettings, HttpUrl
from typing import Dict, Any

class WhatsAppSettings(BaseSettings):
    api_url: HttpUrl
    headers: Dict[str, str]
    timeout_seconds: int = 30
    max_retries: int = 3

class ConversationSettings(BaseSettings):
    timeout_minutes: int = 30
    max_active_conversations: int = 1000

class AppSettings(BaseSettings):
    whatsapp: WhatsAppSettings
    conversation: ConversationSettings
    debug: bool = False
    environment: str = "development"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

## 2. Testing Strategy

### 2.1 Unit Tests

#### Test Structure:
```
tests/
├── unit/
│   ├── test_services/
│   │   ├── test_base_service.py
│   │   ├── test_organization_service.py
│   │   └── ...
│   ├── test_utils/
│   │   ├── test_whatsapp_client.py
│   │   └── test_validators.py
│   └── test_message_handler.py
```

#### Example Test Cases:

1. Service Tests:
```python
def test_organization_service_initial_message():
    service = OrganizationService("test_user")
    messages = service.handle_initial_message()
    
    assert len(messages) == 2
    assert messages[0]["type"] == "text"
    assert messages[1]["type"] == "interactive"

def test_conversation_state_transitions():
    service = OrganizationService("test_user")
    assert service.get_conversation_state() == "initial"
    
    service.handle_initial_message()
    assert service.get_conversation_state() == "awaiting_space_type"
```

2. WhatsApp Client Tests:
```python
def test_whatsapp_client_send_message(mock_requests):
    client = WhatsAppClient(api_url="http://test", headers={})
    mock_requests.post.return_value.status_code = 200
    mock_requests.post.return_value.json.return_value = {"success": True}
    
    response = client.send_message({"test": "payload"})
    assert response["success"] is True
```

### 2.2 Integration Tests

#### Test Structure:
```
tests/
├── integration/
│   ├── test_conversation_flows.py
│   ├── test_api_endpoints.py
│   └── test_whatsapp_integration.py
```

#### Example Test Cases:
```python
def test_complete_organization_flow():
    container = Container()
    service = container.service_factory().create(ServiceType.ORGANIZATION, "test_user")
    
    # Test initial message
    messages = service.handle_initial_message()
    assert len(messages) == 2
    
    # Test space type selection
    response = service.handle_response({
        "interactive": {"button_reply": {"id": "living_room"}}
    })
    assert len(response) == 1
    assert service.get_conversation_state() == "awaiting_pain_points"
```

### 2.3 End-to-End Tests

#### Example Test Cases:
```python
def test_webhook_endpoint():
    client = TestClient(app)
    response = client.post("/hook", json={
        "messages": [{
            "from": "test_user",
            "type": "text",
            "text": {"body": "Hello"}
        }]
    })
    assert response.status_code == 200
    assert response.json()["status"] == "success"
```

## 3. Performance Improvements

### 3.1 Memory Management

#### Implementation Plan:

1. Add Monitoring:
```python
from datadog import statsd

class ConversationManager:
    def __init__(self):
        self.conversations = {}
        
    def add_conversation(self, user_id: str, service: BaseConversationService) -> None:
        self.conversations[user_id] = service
        statsd.gauge("conversations.active", len(self.conversations))
```

2. Implement Cleanup Job:
```python
from apscheduler.schedulers.background import BackgroundScheduler

def setup_cleanup_job(app: Flask, conversation_manager: ConversationManager) -> None:
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        conversation_manager.cleanup_stale_conversations,
        'interval',
        minutes=5
    )
    scheduler.start()
```

### 3.2 Error Handling

#### Implementation Plan:

1. Create Custom Exceptions:
```python
class WhatsAppBotError(Exception):
    """Base exception for WhatsApp bot errors"""
    pass

class WhatsAppAPIError(WhatsAppBotError):
    """Raised when WhatsApp API request fails"""
    pass

class ConversationError(WhatsAppBotError):
    """Raised for conversation-related errors"""
    pass
```

2. Add Error Handlers:
```python
@app.errorhandler(WhatsAppAPIError)
def handle_whatsapp_error(error):
    logger.error(f"WhatsApp API error: {error}")
    return jsonify({"error": str(error)}), 503

@app.errorhandler(ConversationError)
def handle_conversation_error(error):
    logger.error(f"Conversation error: {error}")
    return jsonify({"error": str(error)}), 400
```

### 3.3 Caching

#### Implementation Plan:

1. Add Response Template Caching:
```python
from functools import lru_cache
from typing import Dict

class ResponseTemplates:
    @lru_cache(maxsize=100)
    def get_template(self, template_name: str, language: str = "he") -> Dict:
        return self.load_template(template_name, language)
```

## 4. Code Quality Improvements

### 4.1 Type Hints

Add comprehensive type hints:
```python
from typing import TypeVar, Generic, Protocol

T = TypeVar('T', bound=BaseConversationService)

class ServiceProtocol(Protocol):
    def handle_initial_message(self) -> List[Dict[str, Any]]: ...
    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]: ...
```

### 4.2 Code Style

1. Add pre-commit hooks:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/psf/black
    rev: 21.5b2
    hooks:
      - id: black
        language_version: python3.8
  - repo: https://github.com/pycqa/flake8
    rev: 3.9.2
    hooks:
      - id: flake8
```

2. Add flake8 configuration:
```ini
# setup.cfg
[flake8]
max-line-length = 88
extend-ignore = E203
```

### 4.3 Logging

Add structured logging:
```python
import structlog

logger = structlog.get_logger()

class WhatsAppClient:
    def send_message(self, payload: dict) -> dict:
        logger.info(
            "sending_whatsapp_message",
            recipient=payload.get("to"),
            message_type=payload.get("type")
        )
```

## 5. Documentation Improvements

### 5.1 Code Documentation

Add comprehensive docstrings:
```python
class BaseConversationService(ABC):
    """
    Base class for conversation services.
    
    This class provides the foundation for implementing specific conversation
    flows. Each service should implement the abstract methods to define its
    unique conversation logic.
    
    Attributes:
        recipient (str): The recipient's phone number
        conversation_state (str): Current state of the conversation
    
    Example:
        class MyService(BaseConversationService):
            def get_service_name(self) -> str:
                return "my_service"
                
            def handle_initial_message(self) -> List[Dict[str, Any]]:
                return [self.create_text_message("Welcome!")]
    """
```

### 5.2 API Documentation

Add OpenAPI documentation:
```python
from flask_restx import Api, Resource

api = Api(
    title="WhatsApp Bot API",
    version="1.0",
    description="API for handling WhatsApp bot interactions"
)

@api.route('/hook')
class WebhookEndpoint(Resource):
    @api.expect(webhook_model)
    @api.response(200, 'Success')
    @api.response(500, 'Internal Server Error')
    def post(self):
        """Handle incoming WhatsApp webhook events"""
        pass
```

### 5.3 Developer Documentation

Create developer guides in the docs folder explaining:
- Project setup and installation
- Adding new services
- Testing guidelines
- Deployment procedures
- Monitoring and maintenance

## Implementation Priority

1. Architecture Improvements
   - Service Layer Refinement
   - Dependency Injection
   - Configuration Management

2. Testing Strategy
   - Unit Tests
   - Integration Tests
   - End-to-End Tests

3. Code Quality
   - Type Hints
   - Linting & Formatting
   - Documentation

4. Performance Improvements
   - Memory Management
   - Error Handling
   - Caching

## Next Steps

1. Set up development environment with required tools
2. Implement ConversationManager and ServiceFactory
3. Add dependency injection
4. Set up testing framework
5. Start adding tests while refactoring

Progress will be tracked in GitHub issues and project board.