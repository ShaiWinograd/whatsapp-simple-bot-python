"""Unit tests for state transition monitoring."""
import pytest
from datetime import datetime, timedelta
from ..utils.state_monitor import StateTransitionMonitor, StateTransition

class TestStateTransitionMonitor:
    """Test cases for state transition monitoring"""
    
    @pytest.fixture
    def monitor(self):
        """Monitor fixture"""
        return StateTransitionMonitor()
        
    def test_log_transition(self, monitor):
        """Test logging state transitions"""
        monitor.log_transition(
            user_id='test_user',
            from_state='initial',
            to_state='awaiting_packing_choice',
            flow_type='moving'
        )
        
        history = monitor.get_user_flow_history('test_user')
        assert len(history) == 1
        assert history[0]['from_state'] == 'initial'
        assert history[0]['to_state'] == 'awaiting_packing_choice'
        assert history[0]['flow_type'] == 'moving'
        
    def test_get_flow_metrics(self, monitor):
        """Test flow metrics calculation"""
        # Add multiple transitions
        transitions = [
            ('user1', 'initial', 'awaiting_packing_choice'),
            ('user1', 'awaiting_packing_choice', 'awaiting_verification'),
            ('user1', 'awaiting_verification', 'completed'),
            ('user2', 'initial', 'awaiting_packing_choice'),
            ('user2', 'awaiting_packing_choice', 'initial'),  # Abandoned
        ]
        
        for user_id, from_state, to_state in transitions:
            monitor.log_transition(
                user_id=user_id,
                from_state=from_state,
                to_state=to_state,
                flow_type='moving'
            )
            
        metrics = monitor.get_flow_metrics('moving')
        
        assert metrics['total_users'] == 2
        assert metrics['total_transitions'] == 5
        assert metrics['completion_rate'] == 0.5  # 1 of 2 users completed
        
        # Check common paths
        paths = {p['path']: p['count'] for p in metrics['common_paths']}
        assert paths['initial->awaiting_packing_choice'] == 2
        assert paths['awaiting_packing_choice->awaiting_verification'] == 1
        assert paths['awaiting_verification->completed'] == 1
        
    def test_get_user_flow_history(self, monitor):
        """Test retrieving user flow history"""
        user_id = 'test_user'
        transitions = [
            ('initial', 'awaiting_packing_choice'),
            ('awaiting_packing_choice', 'awaiting_verification'),
            ('awaiting_verification', 'completed')
        ]
        
        for from_state, to_state in transitions:
            monitor.log_transition(
                user_id=user_id,
                from_state=from_state,
                to_state=to_state,
                flow_type='moving'
            )
            
        history = monitor.get_user_flow_history(user_id)
        
        assert len(history) == 3
        for i, (from_state, to_state) in enumerate(transitions):
            assert history[i]['from_state'] == from_state
            assert history[i]['to_state'] == to_state
            
    def test_state_duration_tracking(self, monitor):
        """Test tracking time spent in states"""
        user_id = 'test_user'
        
        # First transition
        monitor.log_transition(
            user_id=user_id,
            from_state='initial',
            to_state='awaiting_packing_choice',
            flow_type='moving'
        )
        
        # Wait before next transition
        monitor._user_states[user_id]['last_transition'] -= timedelta(minutes=5)
        
        # Second transition
        monitor.log_transition(
            user_id=user_id,
            from_state='awaiting_packing_choice',
            to_state='completed',
            flow_type='moving'
        )
        
        history = monitor.get_user_flow_history(user_id)
        
        # First transition has no duration (was initial)
        assert history[0]['duration'] is None
        
        # Second transition should have ~5 minute duration
        duration = datetime.strptime(history[1]['duration'], '%H:%M:%S')
        assert duration.minute == 5