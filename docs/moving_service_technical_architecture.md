# Moving Service Technical Architecture

## Overview

The moving service implements a state machine pattern to handle user interactions through WhatsApp messages. The system processes both interactive button responses and text messages, managing conversation state, labels, and timeouts.

## System Components

```mermaid
graph TB
    subgraph Message Processing
        A[WhatsApp Webhook] --> B[Router]
        B --> C[InteractiveMessageHandler]
        C --> D[ConversationManager]
        
        D --> E{Has Active Flow?}
        E -->|Yes| F[Get Existing Flow]
        E -->|No| G[Create New Flow]
        
        G --> H[BusinessFlowFactory]
        H --> I[MovingFlow Instance]
        
        F --> J[handle_user_input]
        I --> J
        
        J --> K[_handle_state]
        K --> L{Current State?}
    end

    subgraph State Machine
        L -->|initial| M[_handle_initial_state]
        L -->|awaiting_packing_choice| N[_handle_packing_choice]
        L -->|awaiting_customer_details| O[_handle_customer_details]
        L -->|awaiting_verification| P[_handle_verification]
        L -->|awaiting_photos| Q[_handle_photos]
        L -->|awaiting_slot_selection| R[_handle_slot_selection]
        L -->|completed| S[_handle_completed_state]
        
        M --> T[Update State]
        N --> T
        O --> T
        P --> T
        Q --> T
        R --> T
        S --> T
    end

    subgraph Label Management
        U[LabelManager] --> V[WhatsAppClient]
        V --> W[WhatsApp API]
        
        U --> X{Label Operations}
        X -->|Apply| Y[apply_label]
        X -->|Remove| Z[remove_label]
        X -->|Remove All| AA[remove_all_labels]
    end

    subgraph State Management
        BB[StateManager] --> CC{State Operations}
        CC -->|Set| DD[set_state]
        CC -->|Get| EE[get_state]
        CC -->|Remove| FF[remove_state]
        CC -->|Get Flow State| GG[get_flow_state]
    end

    subgraph Key Components
        HH[TimeoutManager]
        II[BusinessFlowManager]
        JJ[ResponseConfig]
        
        HH --> KK[Cleanup Stale Conversations]
        II --> LL[Handle State Transitions]
        JJ --> MM[Message Templates]
    end

    classDef manager fill:#f9f,stroke:#333,stroke-width:2px
    classDef handler fill:#bbf,stroke:#333,stroke-width:2px
    classDef state fill:#bfb,stroke:#333,stroke-width:2px
    classDef flow fill:#ffb,stroke:#333,stroke-width:2px
    
    class D,U,BB,HH,II manager
    class B,C handler
    class L,M,N,O,P,Q,R,S state
    class I flow
```

## Key Components

### 1. Message Processing
- **Router**: Directs incoming webhook notifications to appropriate handlers
- **InteractiveMessageHandler**: Processes button clicks and text inputs
- **ConversationManager**: Coordinates all conversation-related operations

### 2. State Management
The `StateManager` class maintains conversation states:
- Maps user IDs to active business flows
- Provides atomic state operations:
  - `set_state`: Assign a flow to a user
  - `get_state`: Retrieve user's current flow
  - `remove_state`: End user's flow
  - `get_flow_state`: Get current state within flow

### 3. Label Management
The `LabelManager` handles WhatsApp conversation labels:
- Interfaces with WhatsApp API through WhatsAppClient
- Maintains user label history
- Key label operations:
  - `apply_label`: Add a label to conversation
  - `remove_label`: Remove specific label
  - `remove_all_labels`: Clear all labels

### 4. Moving Flow States
The `MovingFlow` class implements the state machine with these states:
1. `initial`: Welcome message and service selection
2. `awaiting_packing_choice`: Service type selection (packing/unpacking/both)
3. `awaiting_customer_details`: Collecting customer information
4. `awaiting_verification`: Verifying provided details
5. `awaiting_photos`: Optional photo submission
6. `awaiting_emergency_support`: Urgent support handling
7. `awaiting_slot_selection`: Call scheduling
8. `completed`: Final state

### 5. Label Transitions
- **New Conversation**: `new_conversation_bot` label applied
- **Moving Service**: `moving` label added when service selected
- **Call Scheduled**: `waiting_for_call` label replaces `new_conversation_bot`
- **Urgent Support**: `waiting_urgent_support` label replaces `new_conversation_bot`
- **Main Menu Return**: All labels removed except `new_conversation_bot`

### 6. Support System
Emergency support flow:
1. User requests support at any stage
2. System prompts for urgency confirmation
3. If urgent:
   - Remove `new_conversation_bot` label
   - Apply `waiting_urgent_support` label
4. If not urgent:
   - Continue to regular call scheduling

### 7. Additional Components
- **TimeoutManager**: Handles conversation expiration
- **BusinessFlowManager**: Manages state transitions
- **ResponseConfig**: Stores message templates
- **BusinessFlowFactory**: Creates appropriate flow instances

## Error Handling
- Input validation at each state
- Timeout management for stale conversations
- Graceful state transitions
- Support request handling at any state

## Configuration
Message templates and responses are externalized in configuration files:
- `moving.py`: Moving service specific responses
- `common.py`: Shared response templates