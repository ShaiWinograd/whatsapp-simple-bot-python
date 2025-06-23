# Moving Service Flow

## Overview
The moving service provides a conversational interface for users to request moving services, including packing, unpacking, or both. The flow is designed to collect necessary information while providing a smooth user experience.

## Detailed Flow

### 1. Initial Contact
- User sends any message to initiate conversation
- System responds with welcome message

### 2. Service Selection
- Moving service is chosen from available services
- System presents packing service options:
  - Packing only 📦
  - Unpacking only 🏡
  - Both packing and unpacking ✨

### 3. Service Details Collection
- Based on selected service, system requests specific details:
  - Full name
  - Current address (for packing/both)
  - New address (for unpacking/both)
  - Email
  - Moving date (or estimated date)

### 4. Details Verification
- System displays provided details for verification
- User can:
  - Approve details ✅ -> Proceed to photo stage
  - Reject details ❌ -> Return to details collection with prompt to rewrite

### 5. Photo Requirement Stage
Two possible paths:

#### Path A: Send Photos
- User sends photos/videos of current home
- Requirements:
  - Open cabinet/closet doors for accurate assessment
  - Photos used only for work scope evaluation

#### Path B: Skip Photos
- User chooses "מעדיפים לוותר על שליחת תמונות" (prefer not to send photos)
- Proceeds directly to scheduling

### 6. Call Scheduling
- System presents available time slots
- User selects preferred time for phone call
- System confirms selected time slot

### 7. Flow Completion
- Conversation marked as completed
- Labels updated:
  - Removes 'bot_new_conversation'
  - Adds 'waiting_call_before_quote'

## State Machine
The conversation follows these states:
1. awaiting_packing_choice
2. awaiting_customer_details
3. awaiting_verification
4. awaiting_photos
5. awaiting_slot_selection
6. completed

## Navigation Options
Throughout the flow, users can:
- Return to main menu
- Request to talk to a representative

## Error Handling
- Invalid inputs trigger appropriate error messages
- Each state has specific validation
- Fallback options available if slot scheduling fails