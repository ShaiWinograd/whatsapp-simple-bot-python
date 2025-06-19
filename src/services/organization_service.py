"""Service for handling home organization conversation flow."""
from typing import List, Dict, Any

from webhook_payload import InteractiveMessagePayload
from src.services.base_service import BaseConversationService


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
        
        welcome_msg = self.create_text_message(
            "אשמח לעזור לך לארגן ולסדר! איזה חלל צריך עזרה?"
        )
        
        options_msg = InteractiveMessagePayload(
            to=self.recipient,
            body="בחר/י מהאפשרויות:",
            button_messages=[
                "חדר שינה/ארון בגדים",
                "מטבח",
                "משרד ביתי",
                "אחר"
            ]
        ).to_dict()
        
        return [welcome_msg, options_msg]

    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle user response based on current conversation state."""
        current_state = self.get_conversation_state()
        
        if current_state == "awaiting_space_type":
            response = message.get('interactive', {}).get('button_reply', {}).get('id', '')
            
            self.set_conversation_state("awaiting_pain_points")
            
            pain_msg = self.create_text_message(
                "מה מפריע לך במצב הנוכחי? מה היית רוצה לשפר?"
            )
            return [pain_msg]
            
        elif current_state == "awaiting_pain_points":
            # After getting pain points, ask about timing
            self.set_conversation_state("awaiting_timing")
            
            timing_msg = self.create_text_message(
                "מתי היית רוצה להתחיל בתהליך?"
            )
            
            options_msg = InteractiveMessagePayload(
                to=self.recipient,
                body="בחר/י:",
                button_messages=[
                    "בשבוע הקרוב",
                    "בחודש הקרוב",
                    "בעתיד, רק מתעניין/ת"
                ]
            ).to_dict()
            
            return [timing_msg, options_msg]
            
        elif current_state == "awaiting_timing":
            # Final message offering consultation
            self.set_conversation_state("completed")
            
            final_msg = self.create_text_message(
                "נשמע מעולה! אשמח להיפגש לפגישת ייעוץ ללא עלות כדי להכיר את המרחב "
                "ולהציע פתרונות מותאמים אישית. האם תרצה/י לקבוע פגישה?"
            )
            
            schedule_msg = InteractiveMessagePayload(
                to=self.recipient,
                body="מתי נוח לך?",
                button_messages=["בוקר", "צהריים", "ערב"]
            ).to_dict()
            
            return [final_msg, schedule_msg]
            
        # Default response if state is unknown
        return [self.create_text_message(
            "מצטערת, לא הבנתי. האם תוכל/י לנסח מחדש?"
        )]