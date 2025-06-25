"""Interactive message handler implementation."""
from typing import Dict, Any, List
from .base_handler import BaseMessageHandler
from ...utils.errors import ConversationError
from ...utils.interactive_message_utils import get_button_title
from ...config.responses.common import GENERAL

# Mapping between Hebrew button titles and flow types
FLOW_TYPE_MAPPING = {
    'מעבר דירה': 'moving',
    'סידור וארגון הבית': 'organization',
    'אשמח לדבר עם נציג/ה': 'support',
    'אחר': 'support'
}


class InteractiveMessageHandler(BaseMessageHandler):
    """Handler for interactive messages and button replies."""

    def handle(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Handle interactive message type and return appropriate response.
        
        Args:
            message (Dict[str, Any]): The incoming WhatsApp message
            base_payload (Dict[str, Any]): Base payload for response message
            
        Returns:
            List[Dict[str, Any]]: List of message payloads to send
        """
        recipient = base_payload["to"]
        print("\nHandling interactive message...")
        print("Full message:", message)

        # Check for existing conversation first for non-interactive messages
        if message.get('type') not in ['interactive', 'reply']:
            conversation_response = self.check_existing_conversation(recipient, message)
            if conversation_response is not None:
                return conversation_response
            return [self.create_welcome_payload(recipient)]

        # Extract button selection
        selected_option = self._get_selected_option(message)
        if not selected_option:
            print("No button selection found in message")
            return [self.create_welcome_payload(recipient)]

        print("Processing selected option:", selected_option)

        # Handle special actions first
        if selected_option == 'חזרה לתפריט הראשי':
            print("User requested main menu")
            self._conversation_manager.remove_conversation(recipient)
            return [self.create_welcome_payload(recipient)]

        # Try to handle the selected option as a flow type
        if selected_option in FLOW_TYPE_MAPPING:
            print(f"Found flow type mapping for: {selected_option}")
            try:
                flow_type = FLOW_TYPE_MAPPING[selected_option]
                print(f"Starting flow of type: {flow_type}")
                
                # Start new conversation with selected flow
                self._conversation_manager.start_conversation(recipient, flow_type)
                
                # Get the flow and its first message
                flow = self._conversation_manager.get_conversation(recipient)
                if flow:
                    return [self.create_flow_message(recipient, flow.get_next_message())]
                    
                print("Failed to create flow")
                return [self.create_text_message(recipient, GENERAL['error'])]
                    
            except ConversationError as e:
                print(f"Error creating flow: {e}")
                return [self.create_welcome_payload(recipient)]

        # Check for existing conversation if no option was handled
        conversation_response = self.check_existing_conversation(recipient, message)
        if conversation_response is not None:
            return conversation_response

        return [self.create_welcome_payload(recipient)]

    def _get_selected_option(self, message: Dict[str, Any]) -> str:
        """Extract the selected option from an interactive message
        
        Args:
            message (Dict[str, Any]): The message to extract from
            
        Returns:
            str: The selected option or empty string if none found
        """
        if 'interactive' in message:
            interactive_data = message.get('interactive', {})
            button_reply = interactive_data.get('button_reply', {})
            if 'title' in button_reply:
                return button_reply['title']
                
        return get_button_title(message)

    def create_welcome_payload(self, recipient: str) -> Dict[str, Any]:
        """Create welcome message with available options
        
        Args:
            recipient (str): The recipient's phone number
            
        Returns:
            Dict[str, Any]: Welcome message payload
        """
        buttons = [
            {'title': 'מעבר דירה'},
            {'title': 'סידור וארגון הבית'},
            {'title': 'אשמח לדבר עם נציג/ה'}
        ]
        
        return self.create_interactive_message(
            recipient=recipient,
            body_text=GENERAL['welcome_message'],
            header_text=GENERAL['header'],
            footer_text=GENERAL['footer'],
            buttons=buttons
        )