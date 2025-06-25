"""Interactive message handler implementation."""
from typing import Dict, Any, List
from .abstract_message_handler import AbstractMessageHandler
from .welcome_handler import WelcomeHandler
from ...utils.errors import ConversationError
from ...whatsapp.utils.message_parser import get_button_title

from ...config.responses.common import NAVIGATION, GENERAL

# Mapping between Hebrew button titles and flow types
FLOW_TYPE_MAPPING = {
    'מעבר דירה': 'moving',
    'סידור וארגון הבית': 'organization',
    'אחר': 'support'
}


class InteractiveMessageHandler(AbstractMessageHandler):
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
        print("\n=== InteractiveMessageHandler.handle() ===")
        print(f"Incoming message: {message}")
        print(f"Base payload: {base_payload}")

        # Check for existing conversation first for non-interactive messages
        if message.get('type') not in ['interactive', 'reply']:
            conversation_response = self.check_existing_conversation(recipient, message)
            if conversation_response is not None:
                return conversation_response
            return WelcomeHandler(self._conversation_manager, self._flow_factory).handle_welcome(recipient)

        # Extract button selection
        selected_option = self._get_selected_option(message)
        print(f"\nExtracted selected option: {selected_option}")
        if not selected_option:
            print("No button selection found in message")
            return WelcomeHandler(self._conversation_manager, self._flow_factory).handle_welcome(recipient)

        print("Processing selected option:", selected_option)

        # Handle navigation actions first
        if selected_option == NAVIGATION['back_to_main']:
            print("User requested main menu")
            self._conversation_manager.remove_conversation(recipient)
            return WelcomeHandler(self._conversation_manager, self._flow_factory).handle_welcome(recipient)
            
        if selected_option == NAVIGATION['talk_to_representative']:
            print("User requested support")
            try:
                # Start support conversation
                self._conversation_manager.start_conversation(recipient, 'support')
                flow = self._conversation_manager.get_conversation(recipient)
                if flow:
                    return [self.create_flow_message(recipient, flow.get_next_message())]
            except ConversationError:
                pass
            return WelcomeHandler(self._conversation_manager, self._flow_factory).handle_welcome(recipient)

        # Try to handle the selected option as a flow type
        if selected_option in FLOW_TYPE_MAPPING:
            print(f"Found flow type mapping for: {selected_option}")
            print(f"Mapped to flow type: {FLOW_TYPE_MAPPING[selected_option]}")
            try:
                flow_type = FLOW_TYPE_MAPPING[selected_option]
                
                # Start new conversation with selected flow
                self._conversation_manager.start_conversation(recipient, flow_type)
                
                # Get the flow and its first message
                flow = self._conversation_manager.get_conversation(recipient)
                print(f"\nCreated flow: {flow.get_flow_name() if flow else None}")
                if flow:
                    next_msg = flow.get_next_message()
                    print(f"Flow's next message: {next_msg}")
                    formatted_msg = self.create_flow_message(recipient, next_msg)
                    print(f"Formatted flow message: {formatted_msg}")
                    return [formatted_msg]
                    
                print("Failed to create flow")
                return [self.create_text_message(recipient, GENERAL['error'])]
                    
            except ConversationError as e:
                print(f"Error creating flow: {e}")
                return WelcomeHandler(self._conversation_manager, self._flow_factory).handle_welcome(recipient)

        # Check for existing conversation if no option was handled
        conversation_response = self.check_existing_conversation(recipient, message)
        if conversation_response is not None:
            return conversation_response

        return WelcomeHandler(self._conversation_manager, self._flow_factory).handle_welcome(recipient)

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