# WhatsApp Bot Documentation

## Documentation Structure

### Architecture and Design
- [System Architecture](system_architecture.md) - System components, class diagrams, and technical details
- [Technical Documentation](technical_documentation.md) - Implementation details and development guide

### Service Flows
- [Moving Service Flow](moving_service_flow.md) - Moving service business flow documentation
- [Organization Service Flow](organization_service_flow.md) - Organization service business flow documentation

## Quick Start

The WhatsApp bot is designed as a modular system with multiple layers:
1. Message processing layer - Handles incoming WhatsApp messages
2. Business logic layer - Manages different service flows
3. State management layer - Handles conversation states and user interactions
4. Integration layer - WhatsApp API integration

## Key Features
- Multiple service flows (Moving, Organization)
- State-based conversation management
- Interactive message support
- Media handling capabilities
- Label-based conversation tracking
- Timeout management
- Error handling and recovery

## Development

### Adding New Features
1. Review the [System Architecture](system_architecture.md) for extension points
2. Follow the patterns in [Technical Documentation](technical_documentation.md)
3. Implement appropriate tests
4. Update documentation as needed

### Key Components
- Message Routing
- Business Flows
- State Management
- WhatsApp Integration