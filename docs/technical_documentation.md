# WhatsApp Bot Technical Documentation

## System Architecture

### Overview
The WhatsApp bot is built using a modular, service-oriented architecture that separates concerns into distinct layers:
- Message Routing Layer
- Service Layer
- State Management Layer
- WhatsApp Integration Layer

### Core Components

#### 1. Message Router (`MessageRouter`)
- **Purpose**: Routes incoming messages to appropriate handlers based on message type
- **Location**: `src/chat/router.py`
- **Supported Message Types**:
  - Text messages
  - Interactive messages (buttons)
  - Reply messages
  - Image messages
  - Video messages
- **Handler Resolution**: Uses a type-to-handler mapping for dynamic dispatch

#### 2. Conversation Manager (`ConversationManager`)
- **Purpose**: Manages conversation state and lifecycle
- **Location**: `src/chat/conversation_manager.py`
- **Features**:
  - Conversation tracking by user ID
  - Timeout management (default: 300 minutes)
  - Active state tracking
  - Automatic cleanup of stale conversations
- **Key Methods**:
  - `add_conversation(user_id, service)`
  - `get_conversation(user_id)`
  - `is_conversation_active(user_id)`
  - `cleanup_stale_conversations()`

#### 3. Service Factory (`ServiceFactory`)
- **Purpose**: Creates service instances using factory pattern
- **Location**: `src/services/service_factory.py`
- **Supported Services**:
  - Organization service
  - Moving service
  - Human support service
- **Features**:
  - Dynamic service registration
  - Type-safe service creation
  - Extensible design for new services

#### 4. Base Service (`BaseConversationService`)
- **Purpose**: Abstract base class for all conversation services
- **Location**: `src/services/base_service.py`
- **Core Features**:
  - State management
  - Message handling
  - Text message creation
- **Abstract Methods**:
  - `get_service_name()`
  - `handle_initial_message()`
  - `handle_response(message)`

### Message Flow

1. **Incoming Message Processing**
```
Webhook → MessageRouter → Appropriate Handler → Service → Response Generation
```

2. **Service Flow**
```
Service → State Check → Process Message → Update State → Generate Response
```

3. **Response Flow**
```
Service → Create Message Payload → WhatsApp Client → User
```

### State Management

#### Conversation States
- Each service maintains its own state machine
- States are string-based identifiers
- State transitions are managed within service implementations
- States persist throughout the conversation lifecycle

#### Data Persistence
- In-memory storage for active conversations
- Timeout-based cleanup for inactive conversations
- State reset on conversation timeout

### Implementation Details

#### 1. Message Handlers
- Each handler type (`TextMessageHandler`, `InteractiveMessageHandler`, etc.) implements specific processing logic
- Handlers receive both message content and base payload
- Response generation is delegated to appropriate service

#### 2. Service Implementation
- Services extend `BaseConversationService`
- Each service defines:
  - State machine logic
  - Message processing rules
  - Response generation
  - Business logic implementation

#### 3. Interactive Messages
- Built using `interactive_message_builder.py`
- Supports:
  - Button responses
  - List responses
  - Dynamic content generation

#### 4. Media Handling
- Supports images and videos
- Media messages are processed through dedicated handlers
- Media URLs are validated and processed accordingly

### Configuration

#### Response Configuration
- Located in `src/config/responses/`
- Modular response definitions per service
- Supports:
  - Text templates
  - Button configurations
  - Dynamic content insertion

#### WhatsApp Integration
- Uses WhatsApp Cloud API
- Configuration via environment variables:
  - API Token
  - API URL
  - Webhook configuration

### Error Handling

#### Types of Errors
1. Message Processing Errors
   - Invalid message format
   - Unsupported message type
   - Missing required fields

2. Service Errors
   - Invalid state transitions
   - Business logic violations
   - Resource unavailability

3. API Errors
   - Communication failures
   - Rate limiting
   - Authentication issues

#### Error Recovery
- Graceful degradation
- User-friendly error messages
- State preservation during errors
- Automatic retry mechanisms where appropriate

### Security

#### Authentication
- WhatsApp API token-based authentication
- Environment-based configuration
- Secure token storage

#### Input Validation
- Message payload validation
- State transition validation
- User input sanitization

### Testing

#### Test Categories
1. Unit Tests
   - Individual component testing
   - Service logic verification
   - State management validation

2. Integration Tests
   - Cross-component interaction
   - End-to-end flow testing
   - API integration verification

### Deployment Considerations

#### Requirements
- Python 3.7+
- WhatsApp Business API access
- Required environment variables
- Proper webhook configuration

#### Monitoring
- Conversation state tracking
- Error logging
- Performance metrics
- User interaction analytics

### Extension Points

#### Adding New Services
1. Create new service class extending `BaseConversationService`
2. Implement required abstract methods
3. Register service with `ServiceFactory`
4. Add response configurations

#### Adding Message Types
1. Create new handler class
2. Add handler to `MessageRouter`
3. Implement processing logic
4. Update service implementations as needed

### Performance Optimization

#### Caching
- In-memory conversation caching
- Response template caching
- Service instance pooling

#### Resource Management
- Automatic cleanup of stale conversations
- Memory usage optimization
- Connection pooling for external services

### Logging and Debugging

#### Debug Information
- State transition logging
- Message flow tracking
- Error tracking with stack traces
- Performance metrics

#### Monitoring Points
- Message processing times
- State transition success rates
- Error frequencies
- User interaction patterns