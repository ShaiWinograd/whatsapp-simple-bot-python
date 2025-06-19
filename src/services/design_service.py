"""Service for handling home design conversation flow."""
from typing import List, Dict, Any

from webhook_payload import InteractiveMessagePayload
from src.services.base_service import BaseConversationService


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
        
        welcome_msg = self.create_text_message(
            "אשמח לעזור לך לעצב את הבית! איזה סוג של פרויקט מעניין אותך?"
        )
        
        options_msg = InteractiveMessagePayload(
            to=self.recipient,
            body="בחר/י מהאפשרויות:",
            button_messages=[
                "עיצוב דירה שלמה",
                "עיצוב חדר ספציפי",
                "ייעוץ צבע וטקסטיל",
                "סטיילינג ואבזור"
            ]
        ).to_dict()
        
        return [welcome_msg, options_msg]

    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle user response based on current conversation state."""
        current_state = self.get_conversation_state()
        
        if current_state == "awaiting_project_type":
            response = message.get('interactive', {}).get('button_reply', {}).get('id', '')
            
            self.set_conversation_state("awaiting_style_preference")
            
            style_msg = self.create_text_message(
                "איזה סגנון עיצובי מדבר אליך?"
            )
            
            options_msg = InteractiveMessagePayload(
                to=self.recipient,
                body="בחר/י:",
                button_messages=[
                    "מודרני ונקי",
                    "חמים וביתי",
                    "סקנדינבי",
                    "אקלקטי"
                ]
            ).to_dict()
            
            return [style_msg, options_msg]
            
        elif current_state == "awaiting_style_preference":
            # After getting style preference, ask about budget
            self.set_conversation_state("awaiting_budget")
            
            budget_msg = self.create_text_message(
                "מה התקציב המשוער שהיית רוצה להשקיע בפרויקט?"
            )
            
            options_msg = InteractiveMessagePayload(
                to=self.recipient,
                body="טווח תקציב:",
                button_messages=[
                    "עד 5,000 ₪",
                    "5,000-15,000 ₪",
                    "15,000-30,000 ₪",
                    "מעל 30,000 ₪"
                ]
            ).to_dict()
            
            return [budget_msg, options_msg]
            
        elif current_state == "awaiting_budget":
            # Final message suggesting consultation
            self.set_conversation_state("completed")
            
            final_msg = self.create_text_message(
                "תודה על השיתוף! כדי שאוכל להבין טוב יותר את הצרכים והחלל, "
                "אשמח להיפגש לפגישת ייעוץ ראשונית. בפגישה נוכל לדבר על הרעיונות שלך "
                "ואוכל להציע כיווני עיצוב מתאימים."
            )
            
            schedule_msg = InteractiveMessagePayload(
                to=self.recipient,
                body="מתי נוח לך להיפגש?",
                button_messages=["בוקר", "צהריים", "ערב"]
            ).to_dict()
            
            return [final_msg, schedule_msg]
            
        # Default response if state is unknown
        return [self.create_text_message(
            "מצטערת, לא הבנתי. האם תוכל/י לנסח מחדש?"
        )]