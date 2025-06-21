"""Service for handling moving home conversation flow."""
from typing import List, Dict, Any

from webhook_payload import InteractiveMessagePayload
from src.services.base_service import BaseConversationService
from src.config.responses import SERVICE_RESPONSES, GENERAL_RESPONSES


class MovingService(BaseConversationService):
    """Service for handling moving home related conversations."""

    def get_service_name(self) -> str:
        return "מעבר דירה"

    def handle_initial_message(self) -> List[Dict[str, Any]]:
        """
        Handle initial moving service conversation.
        
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        self.set_conversation_state("awaiting_packing_choice")
        responses = SERVICE_RESPONSES['moving']['initial']
        
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
        responses = SERVICE_RESPONSES['moving']
        
        if current_state == "awaiting_packing_choice":
            response = message.get('interactive', {}).get('button_reply', {}).get('id', '')
            
            if response in responses['initial']['options']['buttons']:
                self.set_conversation_state("awaiting_move_type")
                move_responses = responses['awaiting_move_type']
                
                location_msg = self.create_text_message(move_responses['question'])
                
                location_options = InteractiveMessagePayload(
                    to=self.recipient,
                    body=move_responses['options']['title'],
                    button_messages=move_responses['options']['buttons']
                ).to_dict()
                
                return [location_msg, location_options]

        elif current_state == "awaiting_move_type":
            response = message.get('interactive', {}).get('button_reply', {}).get('id', '')
            
            if response in responses['awaiting_move_type']['options']['buttons']:
                self.set_conversation_state("awaiting_property_size")
                
                size_msg = self.create_text_message(
                    responses['awaiting_property_size']['question']
                )
                return [size_msg]

        elif current_state == "awaiting_property_size":
            self.set_conversation_state("awaiting_move_date")
            
            date_msg = self.create_text_message(
                responses['awaiting_move_date']['question']
            )
            return [date_msg]
            
        elif current_state == "awaiting_move_date":
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