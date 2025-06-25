# Moving Service Flow

This module implements the WhatsApp chat flow for the moving service.

## Business Flow

The moving service follows this general flow:

1. Initial service selection (packing/unpacking/both)
2. Customer details collection
3. Details verification
4. Photo submission (optional)
5. Time slot selection
6. Confirmation and completion

At any point, users can:
- Return to main menu
- Request emergency support
- Talk to a representative

## Components

### MovingFlow

Main flow controller implementing the state machine for the moving service. States include:

- `initial`: Service type selection
- `awaiting_packing_choice`: Collecting service details
- `awaiting_customer_details`: Address collection
- `awaiting_verification`: Details verification
- `awaiting_photos`: Photo submission
- `awaiting_emergency_support`: Urgent support handling
- `awaiting_slot_selection`: Time slot selection
- `awaiting_reschedule`: Rescheduling handling
- `completed`: Flow completion

### MovingFlowValidator

Input validation for:
- Customer address details
- Photo submissions
- Time slot selections

### Label Management

The flow manages these WhatsApp labels:
- `bot_new_conversation`: Applied at start
- `moving`: Applied when service is selected
- `waiting_urgent_support`: Applied for emergency support
- `waiting_call_before_quote`: Applied at completion

Labels are automatically cleaned up when:
- Returning to main menu
- Starting emergency support
- Flow completion

## State Monitoring

The system tracks:
- State transitions
- Time spent in each state
- Completion rates
- Common paths through the flow
- User journey metrics

## Configuration Validation

All configuration is validated at startup:
- Required WhatsApp labels
- Message templates
- Timeout settings
- Response formats

## Error Handling

The system includes:
- Input validation
- State transition validation
- Configuration validation
- Error recovery paths
- Logging and monitoring

## Testing

Comprehensive test coverage for:
- State transitions
- Input validation
- Label management
- Configuration validation
- State monitoring

## Usage Example

```python
# Initialize flow
flow = MovingFlow()

# Handle user input
next_state = flow.handle_input(user_input)
response = flow.get_next_message()

# Monitor state changes
monitor = StateTransitionMonitor()
monitor.log_transition(
    user_id='user123',
    from_state='initial',
    to_state=next_state,
    flow_type='moving'
)
```

## Metrics and Analytics

The state monitor provides:
- Completion rates by flow type
- Average time in each state
- Common user paths
- Abandonment points
- Success/failure ratios

Access metrics using:
```python
metrics = monitor.get_flow_metrics('moving')
print(f"Completion rate: {metrics['completion_rate']}")
print(f"Average duration: {metrics['avg_state_duration']}")
```

## Configuration

Example configuration validation:
```python
from utils.config_validator import ConfigValidator

# Validate all configuration
ConfigValidator.validate_all()

# Or validate specific components
ConfigValidator.validate_labels()
ConfigValidator.validate_responses(responses, required_fields)
ConfigValidator.validate_timeouts(timeout_minutes)