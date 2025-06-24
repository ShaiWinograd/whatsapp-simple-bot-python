# Test Suite Documentation

This directory contains the test suite for the WhatsApp Simple Bot Python project.

## Structure

```
tests/
├── __init__.py               # Test package initialization
├── conftest.py              # Common test fixtures and configurations
├── services/                # Tests for service implementations
│   ├── test_base_service.py       # Tests for BaseConversationService
│   ├── test_moving_service.py     # Tests for MovingService
│   └── test_organization_service.py # Tests for OrganizationService
```

## Test Coverage

The test suite covers:

- Service initialization and configuration
- State management
- Message handling and validation
- Interactive message creation
- Error handling
- WhatsApp client integration
- Service-specific flows (moving, organization)

## Running Tests

1. Install test dependencies:
```bash
pip install -r requirements.txt
```

2. Run all tests with coverage:
```bash
pytest
```

3. View coverage report:
- Terminal report is displayed after test run
- HTML report is generated in `htmlcov/` directory

## Writing New Tests

When adding new tests:

1. Follow the existing structure in `tests/`
2. Use fixtures from `conftest.py` for common setup
3. Mock external dependencies (WhatsApp client, etc.)
4. Test both success and error cases
5. Verify state transitions
6. Use descriptive test names and docstrings

## Test Configuration

Configuration is managed through `pytest.ini`:
- Test discovery patterns
- Coverage settings
- Environment variables for testing
- Warning filters