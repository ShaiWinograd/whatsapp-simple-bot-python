"""Interactive message handler implementation."""
from typing import Dict, Any, List
from .message_handler_base import MessageHandlerBase
from ...services.service_factory import ServiceType
from ...utils.errors import ConversationError
from ...utils.interactive_message_utils import get_button_title
from ...utils.interactive_message_builder import create_interactive_message
from ...config.responses.common import GENERAL

# Mapping between Hebrew button titles and ServiceType enum values
SERVICE_TYPE_MAPPING = {
    'מעבר דירה': ServiceType.MOVING,
    'סידור וארגון הבית': ServiceType.ORGANIZATION,
    'אשמח לדבר עם נציג/ה': ServiceType.HUMAN_SUPPORT,
    'אחר': ServiceType.HUMAN_SUPPORT
}


class InteractiveMessageHandler(MessageHandlerBase):
    """Handler for interactive messages and button replies."""

    def handle(self, message: Dict[str, Any], base_payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Handle interactive message type and return appropriate response.

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

        # Extract button selection from interactive message
        selected_option = None
        if 'interactive' in message:
            interactive_data = message.get('interactive', {})
            print("Interactive data:", interactive_data)
            
            button_reply = interactive_data.get('button_reply', {})
            selected_option = button_reply.get('title')
            print(f"Button reply - title: {selected_option}")
            
        if not selected_option:
            # Try getting the option from our utility function
            selected_option = get_button_title(message)
            print(f"Got button title from utility: {selected_option}")

        # Process the selected option
        if selected_option:
            print("Processing selected option:", selected_option)
            print("Available mappings:", SERVICE_TYPE_MAPPING)

            # First check for special actions
            if selected_option == 'חזרה לתפריט הראשי':
                print("User requested main menu")
                self.conversation_manager.remove_conversation(recipient)
                return [self.create_welcome_payload(recipient)]

            if selected_option == 'אשמח לדבר עם נציג/ה':
                print("User requested human support")
                service = self.service_factory.create(ServiceType.HUMAN_SUPPORT, recipient, self.conversation_manager)
                self.conversation_manager.add_conversation(recipient, service)
                return service.handle_initial_message()

            # Then check service mappings
            if selected_option in SERVICE_TYPE_MAPPING:
                print(f"Found service type mapping for: {selected_option}")
                try:
                    service_type = SERVICE_TYPE_MAPPING[selected_option]
                    print(f"Creating service of type: {service_type}")
                    service = self.service_factory.create(service_type, recipient, self.conversation_manager)
                    self.conversation_manager.add_conversation(recipient, service)
                    return service.handle_initial_message()
                except ConversationError as e:
                    print(f"Error creating service: {e}")
                    return [self.create_welcome_payload(recipient)]

        # Check for existing conversation if no option was handled
        conversation_response = self.check_existing_conversation(recipient, message)
        if conversation_response is not None:
            return conversation_response

        return [self.create_welcome_payload(recipient)]

    def create_welcome_payload(self, recipient: str) -> Dict[str, Any]:
        """Create a welcome message payload with default buttons."""
        return create_interactive_message(recipient)