"""Unit tests for moving service flow."""
import pytest
from ..business.flows.moving_flow import MovingFlow
from ..business.flows.moving.validator import MovingFlowValidator
from ..business.messages import NAVIGATION, DEFAULT_TIME_SLOTS

class TestMovingFlow:
    """Test cases for moving service flow"""
    
    @pytest.fixture
    def flow(self):
        """Flow fixture"""
        return MovingFlow()
        
    @pytest.fixture
    def validator(self):
        """Validator fixture"""
        return MovingFlowValidator()
        
    def test_initial_state_handling(self, flow):
        """Test initial state transitions"""
        # Test valid service selection
        assert flow.handle_input('אריזת הבית') == 'awaiting_packing_choice'
        assert flow._service_type == 'packing_only'
        
        assert flow.handle_input('סידור בבית החדש') == 'awaiting_packing_choice'
        assert flow._service_type == 'unpacking_only'
        
        assert flow.handle_input('ליווי מלא - אריזה וסידור') == 'awaiting_packing_choice'
        assert flow._service_type == 'both'
        
        # Test invalid input
        flow._conversation_state = 'initial'
        assert flow.handle_input('invalid') == 'initial'
        
    def test_customer_details_validation(self, flow):
        """Test customer details handling"""
        flow._conversation_state = 'awaiting_packing_choice'
        
        # Test valid address
        valid_address = 'רחוב הרצל 5, תל אביב'
        assert flow.handle_input(valid_address) == 'awaiting_verification'
        assert flow._customer_details == valid_address
        
        # Test invalid address (too short)
        flow._conversation_state = 'awaiting_packing_choice'
        assert flow.handle_input('קצר') == 'awaiting_packing_choice'
        
    def test_verification_handling(self, flow):
        """Test verification state handling"""
        flow._conversation_state = 'awaiting_verification'
        flow._customer_details = 'רחוב הרצל 5, תל אביב'
        
        # Test approval
        assert flow.handle_input('כן, הפרטים נכונים') == 'awaiting_photos'
        
        # Test rejection
        flow._conversation_state = 'awaiting_verification'
        assert flow.handle_input('לא, צריך לתקן') == 'awaiting_customer_details'
        
        # Test invalid input
        flow._conversation_state = 'awaiting_verification'
        assert flow.handle_input('invalid') == 'awaiting_verification'
        
    def test_photo_handling(self, flow):
        """Test photo submission handling"""
        flow._conversation_state = 'awaiting_photos'
        
        # Test skip option
        assert flow.handle_input('דלג') == 'awaiting_slot_selection'
        
        # Test valid photo
        flow._conversation_state = 'awaiting_photos'
        photo_data = {'id': 'test_id', 'mime_type': 'image/jpeg'}
        assert flow.handle_input(photo_data) == 'awaiting_slot_selection'
        
        # Test invalid photo
        flow._conversation_state = 'awaiting_photos'
        assert flow.handle_input('invalid') == 'awaiting_photos'
        
    def test_emergency_support_handling(self, flow):
        """Test emergency support handling"""
        flow._conversation_state = 'awaiting_emergency_support'
        
        # Test urgent support
        assert flow.handle_input('כן') == 'completed'
        
        # Test non-urgent support
        flow._conversation_state = 'awaiting_emergency_support'
        assert flow.handle_input('לא') == 'awaiting_slot_selection'
        
    def test_slot_selection_handling(self, flow):
        """Test time slot selection handling"""
        flow._conversation_state = 'awaiting_slot_selection'
        valid_slot = list(DEFAULT_TIME_SLOTS.values())[0]  # Use first available slot
        
        # Test valid slot
        assert flow.handle_input(valid_slot) == 'completed'
        assert flow._selected_time_slot == valid_slot
        
        # Test invalid slot
        flow._conversation_state = 'awaiting_slot_selection'
        assert flow.handle_input('invalid') == 'awaiting_slot_selection'
        
    def test_reschedule_handling(self, flow):
        """Test reschedule handling"""
        flow._conversation_state = 'completed'
        
        # Test reschedule request
        assert flow.handle_input('לקבוע זמן אחר') == 'awaiting_reschedule'
        
        # Test new slot selection
        flow._conversation_state = 'awaiting_reschedule'
        new_slot = list(DEFAULT_TIME_SLOTS.values())[1]  # Use second available slot
        assert flow.handle_input(new_slot) == 'completed'
        assert flow._selected_time_slot == new_slot
        
    def test_global_navigation(self, flow):
        """Test global navigation options"""
        # Test return to main menu from any state
        states = ['awaiting_packing_choice', 'awaiting_customer_details', 
                 'awaiting_verification', 'awaiting_photos', 
                 'awaiting_slot_selection', 'completed']
                 
        for state in states:
            flow._conversation_state = state
            assert flow.handle_input(NAVIGATION['back_to_main']) == 'initial'
            
        # Test support request from any state
        for state in states:
            flow._conversation_state = state
            assert flow.handle_input(NAVIGATION['talk_to_representative']) == 'awaiting_emergency_support'