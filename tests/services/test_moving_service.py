"""Tests for the MovingService class."""
import pytest
from src.services.moving_service import MovingService
from src.config.responses import SERVICE_RESPONSES
from src.config.responses.common import NAVIGATION, GENERAL


@pytest.fixture
def moving_service():
    """Fixture for creating a MovingService instance."""
    return MovingService(recipient="1234567890")


def test_initialization(moving_service):
    """Test MovingService initialization."""
    assert moving_service.recipient == "1234567890"
    assert moving_service.get_conversation_state() == "initial"
    assert moving_service.service_type is None
    assert moving_service.selected_time_slot is None
    assert moving_service.customer_details is None
    assert moving_service.responses == SERVICE_RESPONSES['moving']


def test_get_service_name(moving_service):
    """Test get_service_name returns correct value."""
    assert moving_service.get_service_name() == SERVICE_RESPONSES['moving']['service_name']


def test_handle_initial_message(moving_service, mocker):
    """Test handle_initial_message sets correct state and creates proper message."""
    # Mock the _apply_service_label method
    mocker.patch.object(moving_service, '_apply_service_label')
    
    messages = moving_service.handle_initial_message()
    
    assert moving_service.get_conversation_state() == "awaiting_packing_choice"
    assert len(messages) == 1
    assert messages[0]['type'] == "interactive"
    
    moving_service._apply_service_label.assert_called_once_with('moving')


def test_handle_packing_choice_valid(moving_service):
    """Test handling valid packing choice selections."""
    moving_service.set_conversation_state("awaiting_packing_choice")
    
    test_cases = [
        ("אריזת הבית", "packing"),
        ("סידור בבית החדש", "unpacking"),
        ("ליווי מלא - אריזה וסידור", "both")
    ]
    
    for button_title, expected_type in test_cases:
        messages = moving_service._handle_packing_choice({
            "interactive": {"button_reply": {"title": button_title}}
        })
        
        assert len(messages) == 1
        assert moving_service.service_type == expected_type
        assert moving_service.get_conversation_state() == "awaiting_customer_details"


def test_handle_packing_choice_navigation(moving_service):
    """Test handling navigation options in packing choice."""
    moving_service.set_conversation_state("awaiting_packing_choice")
    
    # Test back to main
    messages = moving_service._handle_packing_choice({
        "interactive": {"button_reply": {"title": NAVIGATION['back_to_main']}}
    })
    assert len(messages) == 1
    
    # Test talk to representative
    messages = moving_service._handle_packing_choice({
        "interactive": {"button_reply": {"title": NAVIGATION['talk_to_representative']}}
    })
    assert len(messages) == 0


def test_get_address_type_for_service(moving_service):
    """Test address type text based on service type."""
    test_cases = [
        ("packing", "כתובת נוכחית"),
        ("unpacking", "כתובת חדשה"),
        ("both", "כתובת נוכחית וחדשה")
    ]
    
    for service_type, expected_text in test_cases:
        moving_service.service_type = service_type
        address_type = moving_service._get_address_type_for_service()
        assert expected_text in address_type


def test_handle_customer_details(moving_service):
    """Test handling customer details submission."""
    moving_service.set_conversation_state("awaiting_customer_details")
    moving_service.service_type = "packing"
    
    # Test empty details
    messages = moving_service._handle_customer_details({"text": {"body": ""}})
    assert len(messages) == 1
    
    # Test too short details
    messages = moving_service._handle_customer_details({"text": {"body": "short"}})
    assert len(messages) == 2
    assert "לא מספיקים" in messages[0]['text']['body']
    
    # Test valid details
    valid_details = "שם: ישראל ישראלי, טלפון: 0501234567, כתובת נוכחית: תל אביב"
    messages = moving_service._handle_customer_details({"text": {"body": valid_details}})
    assert len(messages) == 1
    assert moving_service.customer_details == valid_details
    assert moving_service.get_conversation_state() == "awaiting_verification"


def test_handle_verification(moving_service):
    """Test handling verification responses."""
    moving_service.set_conversation_state("awaiting_verification")
    moving_service.customer_details = "Test details"
    moving_service.service_type = "packing"
    
    # Test confirmation
    messages = moving_service._handle_verification({
        "interactive": {"button_reply": {"title": "כן, הפרטים נכונים"}}
    })
    assert len(messages) == 2  # Photo requirement message and options
    assert moving_service.get_conversation_state() == "awaiting_photos"
    
    # Test correction
    messages = moving_service._handle_verification({
        "interactive": {"button_reply": {"title": "לא, צריך לתקן"}}
    })
    assert len(messages) == 1
    assert moving_service.customer_details is None
    assert moving_service.get_conversation_state() == "awaiting_customer_details"


def test_handle_photos(moving_service):
    """Test handling photo submissions."""
    moving_service.set_conversation_state("awaiting_photos")
    
    # Test valid image submission
    messages = moving_service._handle_photos({
        "type": "image",
        "image": {"id": "test_image_id"}
    })
    assert len(messages) == 1
    assert moving_service.get_conversation_state() == "awaiting_slot_selection"
    
    # Test valid video submission
    messages = moving_service._handle_photos({
        "type": "video",
        "video": {"id": "test_video_id"}
    })
    assert len(messages) == 1
    assert moving_service.get_conversation_state() == "awaiting_slot_selection"
    assert moving_service.get_conversation_state() == "awaiting_slot_selection"
    
    # Test skip photos option
    messages = moving_service._handle_photos({
        "interactive": {"button_reply": {"title": "מעדיפים לדלג"}}
    })
    assert len(messages) == 1
    
    # Test invalid submission
    messages = moving_service._handle_photos({
        "text": {"body": "not a photo"}
    })
    assert len(messages) == 2  # Reminder message and options


def test_handle_invalid_state(moving_service):
    """Test handling invalid state."""
    moving_service.set_conversation_state("invalid_state")
    
    messages = moving_service.handle_response({"text": {"body": "test"}})
    
    assert len(messages) == 1
    assert moving_service.get_conversation_state() == "awaiting_packing_choice"


def test_handle_response_error(moving_service):
    """Test handling response with error."""
    moving_service.set_conversation_state("awaiting_verification")
    
    # Test with invalid message format
    messages = moving_service.handle_response({})
    
    assert len(messages) == 1
    assert messages[0]['text']['body'] == GENERAL['error']


def test_handle_emergency_support(moving_service, mocker):
    """Test handling emergency support inquiry."""
    moving_service.set_conversation_state("awaiting_emergency_support")
    mock_remove_label = mocker.patch.object(moving_service, '_remove_label')
    mock_apply_label = mocker.patch.object(moving_service, '_apply_service_label')

    # Test urgent support
    messages = moving_service._handle_emergency_support({
        "interactive": {"button_reply": {"title": "כן"}}
    })
    assert len(messages) == 1
    assert messages[0]['text']['body'] == moving_service.responses['urgent_support_message']
    mock_remove_label.assert_called_once_with('new_conversation')
    mock_apply_label.assert_called_once_with('waiting_urgent_support')

    # Test non-urgent support
    mock_remove_label.reset_mock()
    mock_apply_label.reset_mock()
    messages = moving_service._handle_emergency_support({
        "interactive": {"button_reply": {"title": "לא"}}
    })
    assert len(messages) == 1
    assert moving_service.get_conversation_state() == "awaiting_slot_selection"
    mock_remove_label.assert_not_called()
    mock_apply_label.assert_not_called()


def test_handle_slot_selection(moving_service, mocker):
    """Test handling time slot selection."""
    moving_service.set_conversation_state("awaiting_slot_selection")
    mock_remove_label = mocker.patch.object(moving_service, '_remove_label')
    mock_apply_label = mocker.patch.object(moving_service, '_apply_service_label')

    # Test valid slot selection
    slot = "היום בין 12:00-14:00"
    messages = moving_service._handle_slot_selection({
        "interactive": {"button_reply": {"title": slot}}
    })
    assert len(messages) == 1
    assert moving_service.selected_time_slot == slot
    assert moving_service.get_conversation_state() == "completed"
    mock_remove_label.assert_called_once_with('new_conversation')
    mock_apply_label.assert_called_once_with('waiting_for_call')

    # Test reschedule
    mock_remove_label.reset_mock()
    mock_apply_label.reset_mock()
    messages = moving_service._handle_slot_selection({
        "interactive": {"button_reply": {"title": "לקבוע זמן אחר"}}
    })
    assert len(messages) == 1
    assert moving_service.get_conversation_state() == "awaiting_slot_selection"
    mock_remove_label.assert_not_called()
    mock_apply_label.assert_not_called()

    # Test talk to representative
    messages = moving_service._handle_slot_selection({
        "interactive": {"button_reply": {"title": NAVIGATION['talk_to_representative']}}
    })
    assert len(messages) == 1
    assert moving_service.get_conversation_state() == "awaiting_emergency_support"