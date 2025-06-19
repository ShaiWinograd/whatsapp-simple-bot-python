"""Service for handling moving home conversation flow."""
from typing import List, Dict, Any

from webhook_payload import InteractiveMessagePayload
from src.services.base_service import BaseConversationService


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
        print(f"MovingService: Starting initial conversation with {self.recipient}")
        self.set_conversation_state("awaiting_packing_choice")
        
        welcome_msg = self.create_text_message(
            "שמחה לעזור בתהליך המעבר! 🏠\n\n"
            "השירות שלנו כולל:\n"
            "- סידור וארגון לפני האריזה\n"
            "- אריזה מקצועית של כל הבית\n"
            "- פריקה וסידור בבית החדש\n"
            "- ליווי וייעוץ לאורך כל התהליך"
        )
        
        print(f"MovingService: Created welcome message")
        
        options_msg = InteractiveMessagePayload(
            to=self.recipient,
            body="איזה סוג עזרה את/ה צריכ/ה?",
            button_messages=["אריזה", "פריקה", "גם אריזה וגם פריקה"]
        ).to_dict()
        
        print(f"MovingService: Created options message")
        
        return [welcome_msg, options_msg]

    def handle_response(self, message: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle user response based on current conversation state."""
        current_state = self.get_conversation_state()
        
        if current_state == "awaiting_packing_choice":
            response = message.get('interactive', {}).get('button_reply', {}).get('id', '')
            
            if response in ["אריזה", "פריקה", "גם אריזה וגם פריקה"]:
                self.set_conversation_state("awaiting_move_type")
                
                location_msg = self.create_text_message(
                    "האם מדובר במעבר בתוך הארץ או מעבר מחו״ל?"
                )
                
                location_options = InteractiveMessagePayload(
                    to=self.recipient,
                    body="אנא בחר/י:",
                    button_messages=["מעבר בתוך הארץ", "מעבר מחו״ל"]
                ).to_dict()
                
                return [location_msg, location_options]

        elif current_state == "awaiting_move_type":
            response = message.get('interactive', {}).get('button_reply', {}).get('id', '')
            
            if response in ["מעבר בתוך הארץ", "מעבר מחו״ל"]:
                self.set_conversation_state("awaiting_property_size")
                
                size_msg = self.create_text_message(
                    "מה גודל הדירה בערך? (במ״ר)"
                )
                return [size_msg]

        elif current_state == "awaiting_property_size":
            # Store size and ask about timing
            self.set_conversation_state("awaiting_move_date")
            
            date_msg = self.create_text_message(
                "מתי בערך מתוכנן המעבר?"
            )
            return [date_msg]
            
        elif current_state == "awaiting_move_date":
            # Final message with next steps
            self.set_conversation_state("completed")
            
            final_msg = self.create_text_message(
                "תודה על הפרטים! אשמח לקבוע פגישת ייעוץ כדי לדבר על התהליך בפירוט "
                "ולהבין איך אני יכולה לעזור. האם את/ה פנוי/ה לשיחה בימים הקרובים?"
            )
            
            options_msg = InteractiveMessagePayload(
                to=self.recipient,
                body="מתי נוח לך?",
                button_messages=["הבוקר", "אחה״צ", "הערב"]
            ).to_dict()
            
            return [final_msg, options_msg]
            
        # Default response if state is unknown
        return [self.create_text_message(
            "מצטערת, לא הבנתי. האם תוכל/י לנסח מחדש?"
        )]