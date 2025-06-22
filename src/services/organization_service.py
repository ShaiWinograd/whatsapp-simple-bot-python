"""Service for handling home organization conversation flow."""
from typing import List, Dict, Any
from ..models.webhook_payload import InteractiveMessagePayload
from .base_service import BaseConversationService
from ..config.responses import SERVICE_RESPONSES, GENERAL_RESPONSES



class OrganizationService(BaseConversationService):
    """Service for handling home organization related conversations."""

    def get_service_name(self) -> str:
        return "סידור וארגון"

    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """
        Handle initial organization service conversation.
        
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        self.set_conversation_state("awaiting_space_type")
        responses = SERVICE_RESPONSES['organization']['initial']
        
        welcome_msg = self.create_text_message(responses['welcome'])
        
        options_msg = InteractiveMessagePayload(
            to=self.recipient,
            body=responses['options']['title'],
            button_messages=responses['options']['buttons']
        ).to_dict()
        
        return [welcome_msg, options_msg]

    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle user response based on current conversation state."""
        current_state = self.get_conversation_state()
        responses = SERVICE_RESPONSES['organization']
        
        if current_state == "awaiting_space_type":
            response = message.get('interactive', {}).get('button_reply', {}).get('id', '')
            self.set_conversation_state("awaiting_pain_points")
            
            pain_msg = self.create_text_message(
                responses['awaiting_pain_points']['question']
            )
            return [pain_msg]
            
        elif current_state == "awaiting_pain_points":
            self.set_conversation_state("awaiting_timing")
            timing_responses = responses['awaiting_timing']
            
            timing_msg = self.create_text_message(timing_responses['question'])
            
            options_msg = InteractiveMessagePayload(
                to=self.recipient,
                body=timing_responses['options']['title'],
                button_messages=timing_responses['options']['buttons']
            ).to_dict()
            
            return [timing_msg, options_msg]
            
        elif current_state == "awaiting_timing":
            self.set_conversation_state("completed")
            completion_responses = responses['completed']
            
            final_msg = self.create_text_message(completion_responses['final'])
            
            schedule_msg = InteractiveMessagePayload(
                to=self.recipient,
                body=completion_responses['schedule']['title'],
                button_messages=completion_responses['schedule']['buttons']
            ).to_dict()
            
            return [final_msg, schedule_msg]
            
        # Default response if state is unknown
        return [self.create_text_message(GENERAL_RESPONSES['error'])]