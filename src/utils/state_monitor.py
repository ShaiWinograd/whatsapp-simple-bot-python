"""State transition monitoring and metrics."""
import logging
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from dataclasses import dataclass
from collections import defaultdict

logger = logging.getLogger(__name__)

@dataclass
class StateTransition:
    """State transition event data"""
    user_id: str
    from_state: str
    to_state: str
    timestamp: datetime
    flow_type: str
    duration: Optional[timedelta] = None

class StateTransitionMonitor:
    """Monitors and tracks state transitions"""
    
    def __init__(self):
        self._transitions: List[StateTransition] = []
        self._user_states: Dict[str, Dict] = defaultdict(dict)
        
    def log_transition(self, user_id: str, from_state: str, 
                      to_state: str, flow_type: str) -> None:
        """Log a state transition
        
        Args:
            user_id: User identifier
            from_state: Previous state
            to_state: New state
            flow_type: Type of business flow
        """
        now = datetime.now()
        
        # Calculate duration in previous state
        duration = None
        if user_id in self._user_states:
            last_transition = self._user_states[user_id].get('last_transition')
            if last_transition:
                duration = now - last_transition
                
        # Create transition record
        transition = StateTransition(
            user_id=user_id,
            from_state=from_state,
            to_state=to_state,
            timestamp=now,
            flow_type=flow_type,
            duration=duration
        )
        
        # Update user state tracking
        self._user_states[user_id].update({
            'current_state': to_state,
            'last_transition': now,
            'flow_type': flow_type
        })
        
        # Store transition
        self._transitions.append(transition)
        
        # Log transition
        logger.info(
            f"State transition: {from_state} -> {to_state} "
            f"(user: {user_id}, flow: {flow_type})"
        )
        
        # Update metrics
        self._update_metrics(transition)
        
    def get_user_flow_history(self, user_id: str) -> List[Dict]:
        """Get state transition history for a user
        
        Args:
            user_id: User identifier
            
        Returns:
            List of transition records
        """
        user_transitions = [
            t for t in self._transitions
            if t.user_id == user_id
        ]
        
        def format_duration(td: Optional[timedelta]) -> Optional[str]:
            if not td:
                return None
            # Convert to total seconds and extract hours, minutes, seconds
            total_seconds = int(td.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60
            return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        
        return [
            {
                'from_state': t.from_state,
                'to_state': t.to_state,
                'timestamp': t.timestamp.isoformat(),
                'duration': format_duration(t.duration),
                'flow_type': t.flow_type
            }
            for t in user_transitions
        ]
        
    def get_flow_metrics(self, flow_type: str,
                        start_time: Optional[datetime] = None,
                        end_time: Optional[datetime] = None) -> Dict:
        """Get metrics for a specific flow type
        
        Args:
            flow_type: Type of business flow
            start_time: Start of time window
            end_time: End of time window
            
        Returns:
            Dictionary of flow metrics
        """
        # Filter transitions by time window
        transitions = [
            t for t in self._transitions
            if t.flow_type == flow_type
            and (not start_time or t.timestamp >= start_time)
            and (not end_time or t.timestamp <= end_time)
        ]
        
        if not transitions:
            return {}
            
        # Calculate metrics
        total_users = len(set(t.user_id for t in transitions))
        completion_rate = len([
            t for t in transitions
            if t.to_state == 'completed'
        ]) / total_users if total_users > 0 else 0
        
        avg_duration = timedelta()
        duration_count = 0
        for t in transitions:
            if t.duration:
                avg_duration += t.duration
                duration_count += 1
        if duration_count > 0:
            avg_duration = avg_duration / duration_count
            
        return {
            'total_users': total_users,
            'total_transitions': len(transitions),
            'completion_rate': completion_rate,
            'avg_state_duration': str(avg_duration),
            'common_paths': self._get_common_paths(transitions),
            'state_distribution': self._get_state_distribution(transitions)
        }
        
    def _update_metrics(self, transition: StateTransition) -> None:
        """Update metrics for a transition
        
        Args:
            transition: State transition event
        """
        try:
            # This would integrate with your metrics collection system
            # For example, using Prometheus or similar:
            metrics = {
                f"state_transition.{transition.from_state}.{transition.to_state}": 1,
                f"state_duration.{transition.from_state}": 
                    transition.duration.total_seconds() if transition.duration else 0
            }
            
            logger.debug(f"Updated metrics: {json.dumps(metrics)}")
            
        except Exception as e:
            logger.error(f"Error updating metrics: {str(e)}")
            
    def _get_common_paths(self, transitions: List[StateTransition]) -> List[Dict]:
        """Get most common state transition paths
        
        Args:
            transitions: List of transitions to analyze
            
        Returns:
            List of common paths with counts
        """
        paths = defaultdict(int)
        for t in transitions:
            path = f"{t.from_state}->{t.to_state}"
            paths[path] += 1
            
        return [
            {'path': path, 'count': count}
            for path, count in sorted(
                paths.items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]  # Top 10 most common
        ]
        
    def _get_state_distribution(self, transitions: List[StateTransition]) -> Dict:
        """Get distribution of time spent in each state
        
        Args:
            transitions: List of transitions to analyze
            
        Returns:
            Dictionary of state durations
        """
        state_durations = defaultdict(timedelta)
        state_counts = defaultdict(int)
        
        for t in transitions:
            if t.duration:
                state_durations[t.from_state] += t.duration
                state_counts[t.from_state] += 1
                
        return {
            state: {
                'total_duration': str(duration),
                'avg_duration': str(duration / state_counts[state])
                if state_counts[state] > 0 else '0:00:00'
            }
            for state, duration in state_durations.items()
        }