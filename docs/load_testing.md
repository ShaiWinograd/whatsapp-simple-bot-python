# Load Testing Guide

This document describes how to perform load testing on the WhatsApp bot system.

## Prerequisites

- [locust](https://locust.io/) for load testing
- Python 3.7+
- Access to test WhatsApp Business API instance

## Setup

1. Install locust:
```bash
pip install locust
```

2. Copy the load test configuration:
```bash
cp tests/load/locustfile.py.template tests/load/locustfile.py
```

3. Configure test parameters in `locustfile.py`:
```python
# Test user patterns
users = [
    {"phone": "1234567890", "name": "Test User 1"},
    {"phone": "0987654321", "name": "Test User 2"}
]

# Test scenarios
scenarios = [
    "full_moving_flow",
    "emergency_support",
    "reschedule_flow"
]
```

## Running Tests

1. Start the locust server:
```bash
locust -f tests/load/locustfile.py
```

2. Open http://localhost:8089 in your browser

3. Configure test parameters:
- Number of users
- Spawn rate
- Host URL

## Test Scenarios

### Full Moving Flow
Tests complete moving service flow:
1. Service selection
2. Details collection
3. Verification
4. Photo upload
5. Time slot selection

### Emergency Support
Tests emergency support flow from various states

### Reschedule Flow
Tests appointment rescheduling functionality

## Monitoring

Monitor these metrics during load testing:
- Response times
- Error rates
- CPU usage
- Memory usage
- Database connections
- WhatsApp API rate limits

## Performance Targets

- Response Time: < 2 seconds
- Error Rate: < 1%
- Concurrent Users: 1000
- Messages/Second: 100

## Common Issues

1. WhatsApp API Rate Limiting
- Monitor rate limit headers
- Implement exponential backoff
- Use message queuing

2. Database Connection Pool
- Monitor connection usage
- Adjust pool size as needed
- Implement connection timeout

3. Memory Usage
- Monitor for memory leaks
- Implement proper cleanup
- Use profiling tools

## Reporting

Generate test reports using:
```bash
locust --headless -f tests/load/locustfile.py --csv=report
```

Reports include:
- Response time statistics
- Error rates
- Request counts
- User counts