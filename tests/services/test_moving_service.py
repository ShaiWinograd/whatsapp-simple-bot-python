"""Tests for the MovingService class."""
import pytest
from src.services.moving_service import MovingService
from src.config.responses import SERVICE_RESPONSES
from src.config.responses.common import NAVIGATION, GENERAL
from src.chat.conversation_manager import ConversationManager


@pytest.fixture
def mock_conversation_manager(mocker):
    """Fixture for creating a mocked ConversationManager."""
    manager = mocker.Mock(spec=ConversationManager)
    return manager


@pytest.fixture
def moving_service(mock_conversation_manager):
    """Fixture for creating a MovingService instance with mocked conversation manager."""
    return MovingService(recipient="1234567890", conversation_manager=mock_conversation_manager)


@pytest.fixture
def moving_service_no_manager():
    """Fixture for creating a MovingService instance without conversation manager."""
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


def test_handle_initial_message_with_manager(moving_service, mock_conversation_manager):
    """Test handle_initial_message with conversation manager."""
    messages = moving_service.handle_initial_message()
    
    mock_conversation_manager.update_service_state.assert_called_once_with(
        "1234567890", "awaiting_packing_choice"
    )
    assert len(messages) == 1
    assert "action" in messages[0]
    assert "buttons" in messages[0]["action"]


def test_handle_initial_message_without_manager(moving_service_no_manager):
    """Test handle_initial_message without conversation manager."""
    messages = moving_service_no_manager.handle_initial_message()
    
    assert moving_service_no_manager.get_conversation_state() == "awaiting_packing_choice"
    assert len(messages) == 1
    assert "action" in messages[0]
    assert "buttons" in messages[0]["action"]


def test_handle_packing_choice_valid(moving_service, mock_conversation_manager):
    """Test handling valid packing choice selections."""
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
        mock_conversation_manager.update_service_state.assert_called_with(
            "1234567890", "awaiting_customer_details"
        )


def test_handle_packing_choice_navigation(moving_service, mock_conversation_manager):
    """Test handling navigation options in packing choice."""
    # Test talk to representative
    messages = moving_service._handle_packing_choice({
        "interactive": {"button_reply": {"title": NAVIGATION['talk_to_representative']}}
    })
    
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_emergency_support"
    )


def test_handle_emergency_support(moving_service, mock_conversation_manager):
    """Test handling emergency support inquiry."""
    # Test urgent support
    messages = moving_service._handle_emergency_support({
        "interactive": {"button_reply": {"title": "כן"}}
    })
    
    assert len(messages) == 1
    assert messages[0]['body'] == moving_service.responses['urgent_support_message']
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_emergency_support"
    )

    # Test non-urgent support
    messages = moving_service._handle_emergency_support({
        "interactive": {"button_reply": {"title": "לא"}}
    })
    
    assert len(messages) == 1
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_slot_selection"
    )


def test_handle_photos_media(moving_service, mock_conversation_manager):
    """Test handling photo and video submissions."""
    # Test valid image submission
    messages = moving_service._handle_photos({
        "type": "image",
        "image": {"id": "test_image_id"}
    })
    
    assert len(messages) == 1
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_slot_selection"
    )


def test_handle_slot_selection_complete(moving_service, mock_conversation_manager):
    """Test complete flow of slot selection."""
    # Test valid slot selection
    slot = "היום בין 12:00-14:00"
    messages = moving_service._handle_slot_selection({
        "interactive": {"button_reply": {"title": slot}}
    })
    
    assert len(messages) == 1
    assert moving_service.selected_time_slot == slot
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "completed"
    )


def test_state_transitions_normal_flow(moving_service, mock_conversation_manager):
    """Test state transitions in normal conversation flow."""
    # Initial -> Packing Choice
    messages = moving_service.handle_initial_message()
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_packing_choice"
    )
    
    # Packing Choice -> Customer Details
    messages = moving_service._handle_packing_choice({
        "interactive": {"button_reply": {"title": "אריזת הבית"}}
    })
    assert moving_service.service_type == "packing"
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_customer_details"
    )
    
    # Slot Selection -> Completed
    messages = moving_service._handle_slot_selection({
        "interactive": {"button_reply": {"title": "היום בין 12:00-14:00"}}
    })
    assert moving_service.selected_time_slot == "היום בין 12:00-14:00"
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "completed"
    )


def test_reset_state_management(moving_service, mock_conversation_manager):
    """Test complete state reset when returning to main menu."""
    # Setup initial state
    moving_service.service_type = "packing"
    moving_service.selected_time_slot = "test slot"
    moving_service.customer_details = "test details"
    
    # Trigger reset
    messages = moving_service._reset_to_main_menu()
    
    # Verify all state is reset
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "initial"
    )
    assert moving_service.service_type is None
    assert moving_service.selected_time_slot is None
    assert moving_service.customer_details is None
    
    # Verify welcome message is returned
    assert len(messages) == 1
    assert "action" in messages[0]
    assert "buttons" in messages[0]["action"]


def test_customer_details_handling(moving_service, mock_conversation_manager):
    """Test handling customer details submission and verification."""
    # Test details submission
    details = "Test customer details"
    messages = moving_service._handle_customer_details({
        "text": {
            "body": details
        }
    })
    
    assert moving_service.customer_details == details
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_verification"
    )
    
    # Test verification
    messages = moving_service._handle_verification({
        "interactive": {"button_reply": {"title": "כן"}}
    })
    
    mock_conversation_manager.update_service_state.assert_called_with(
        "1234567890", "awaiting_photos"
    )