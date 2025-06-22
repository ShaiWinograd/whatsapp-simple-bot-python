"""Service for handling home design conversation flow."""
from typing import List, Dict, Any
from ..models.webhook_payload import InteractiveMessagePayload
from .base_service import BaseConversationService
from ..config.responses import SERVICE_RESPONSES, GENERAL_RESPONSES



class DesignService(BaseConversationService):
    """Service for handling home design related conversations."""

    def get_service_name(self) -> str:
        return "עיצוב והלבשת הבית"

    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """
        Handle initial design service conversation.
        
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        self.set_conversation_state("awaiting_project_type")
        responses = SERVICE_RESPONSES['design']['initial']
        
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
        responses = SERVICE_RESPONSES['design']
        
        if current_state == "awaiting_project_type":
            response = message.get('interactive', {}).get('button_reply', {}).get('id', '')
            self.set_conversation_state("awaiting_style_preference")
            
            style_responses = responses['awaiting_style_preference']
            style_msg = self.create_text_message(style_responses['question'])
            
            options_msg = InteractiveMessagePayload(
                to=self.recipient,
                body=style_responses['options']['title'],
                button_messages=style_responses['options']['buttons']
            ).to_dict()
            
            return [style_msg, options_msg]
            
        elif current_state == "awaiting_style_preference":
            self.set_conversation_state("awaiting_budget")
            budget_responses = responses['awaiting_budget']
            
            budget_msg = self.create_text_message(budget_responses['question'])
            
            options_msg = InteractiveMessagePayload(
                to=self.recipient,
                body=budget_responses['options']['title'],
                button_messages=budget_responses['options']['buttons']
            ).to_dict()
            
            return [budget_msg, options_msg]
            
        elif current_state == "awaiting_budget":
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