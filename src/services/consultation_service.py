"""Service for handling consultation conversation flow."""
from typing import List, Dict, Any
from ..models.webhook_payload import InteractiveMessagePayload
from .base_service import BaseConversationService
from ..config.responses import SERVICE_RESPONSES, GENERAL_RESPONSES



class ConsultationService(BaseConversationService):
    """Service for handling consultation related conversations."""

    def get_service_name(self) -> str:
        return "שיחת ייעוץ"

    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """
        Handle initial consultation conversation.
        
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        self.set_conversation_state("awaiting_consultation_topic")
        responses = SERVICE_RESPONSES['consultation']['initial']
        
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
        responses = SERVICE_RESPONSES['consultation']
        
        if current_state == "awaiting_consultation_topic":
            response = message.get('interactive', {}).get('button_reply', {}).get('id', '')
            self.set_conversation_state("awaiting_questions")
            
            questions_msg = self.create_text_message(
                responses['awaiting_questions']['question']
            )
            return [questions_msg]
            
        elif current_state == "awaiting_questions":
            self.set_conversation_state("awaiting_consultation_type")
            consultation_responses = responses['awaiting_consultation_type']
            
            type_msg = self.create_text_message(consultation_responses['question'])
            
            options_msg = InteractiveMessagePayload(
                to=self.recipient,
                body=consultation_responses['options']['title'],
                button_messages=consultation_responses['options']['buttons']
            ).to_dict()
            
            return [type_msg, options_msg]
            
        elif current_state == "awaiting_consultation_type":
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