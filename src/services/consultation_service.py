"""Service for handling consultation conversation flow."""
from typing import List, Dict, Any

from webhook_payload import InteractiveMessagePayload
from src.services.base_service import BaseConversationService


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
        
        welcome_msg = self.create_text_message(
            "אשמח לקיים איתך שיחת ייעוץ! על מה היית רוצה לדבר?"
        )
        
        options_msg = InteractiveMessagePayload(
            to=self.recipient,
            body="בחר/י נושא:",
            button_messages=[
                "תכנון מעבר דירה",
                "ארגון הבית",
                "עיצוב הבית",
                "אחר"
            ]
        ).to_dict()
        
        return [welcome_msg, options_msg]

    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle user response based on current conversation state."""
        current_state = self.get_conversation_state()
        
        if current_state == "awaiting_consultation_topic":
            response = message.get('interactive', {}).get('button_reply', {}).get('id', '')
            
            self.set_conversation_state("awaiting_questions")
            
            questions_msg = self.create_text_message(
                "האם יש שאלות ספציפיות שהיית רוצה שנדבר עליהן בשיחה?"
            )
            return [questions_msg]
            
        elif current_state == "awaiting_questions":
            # After getting questions, ask about preferred consultation type
            self.set_conversation_state("awaiting_consultation_type")
            
            type_msg = self.create_text_message(
                "איך היית מעדיף/ה לקיים את הפגישה?"
            )
            
            options_msg = InteractiveMessagePayload(
                to=self.recipient,
                body="בחר/י:",
                button_messages=[
                    "פגישה פרונטלית",
                    "שיחת וידאו",
                    "שיחת טלפון"
                ]
            ).to_dict()
            
            return [type_msg, options_msg]
            
        elif current_state == "awaiting_consultation_type":
            # Final message to schedule
            self.set_conversation_state("completed")
            
            final_msg = self.create_text_message(
                "מעולה! אשמח לקבוע איתך את שיחת הייעוץ. "
                "פגישת ייעוץ ראשונית היא ללא עלות ונמשכת כ-45 דקות."
            )
            
            schedule_msg = InteractiveMessagePayload(
                to=self.recipient,
                body="מתי נוח לך?",
                button_messages=[
                    "בימי ראשון-שלישי",
                    "בימי רביעי-חמישי",
                    "ביום שישי"
                ]
            ).to_dict()
            
            return [final_msg, schedule_msg]
            
        # Default response if state is unknown
        return [self.create_text_message(
            "מצטערת, לא הבנתי. האם תוכל/י לנסח מחדש?"
        )]