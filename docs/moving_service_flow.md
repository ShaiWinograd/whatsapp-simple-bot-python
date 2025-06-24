# Moving Service Flow

## Overview
The moving service provides a conversational interface for users to request moving services, including packing, unpacking, or both. The flow is designed to collect necessary information while providing a smooth user experience.

## Label Management

### Initial Label
- `bot_new_conversation`: Applied to each new conversation

### Label Transitions
1. Support Request:
   - Removes: `bot_new_conversation`
   - Applies: `waiting_for_support_urgent`
   - Trigger: User selects "Talk to representative" option
   - System sends message: "נציג שירות יצור איתך קשר בהקדם"

2. Flow Completion:
   - Removes: `bot_new_conversation`
   - Applies: `waiting_call_before_quote`
   - Trigger: User selects time slot for call

## Detailed Flow

### 1. Initial Contact
- User sends any message to initiate conversation
- System applies `bot_new_conversation` label
- System responds with welcome message and header "מעבר דירה 🏠"
- Initial state: `awaiting_packing_choice`

### 2. Service Selection
- User presented with service options:
  * "אריזת הבית 📦" (Packing only)
  * "סידור בבית החדש 🏡" (Unpacking only)
  * "ליווי מלא - אריזה וסידור ✨" (Both packing and unpacking)
  * Back to main menu option
  * Talk to representative option
- Each selection triggers specific price quote form with relevant address requirements

### 3. Service Details Collection
Based on selected service, system requests specific details with different address requirements:
- For Packing Only:
  * Full name
  * Current address (including city, street, house number)
  * Email
  * Moving date (or estimated date)

- For Unpacking Only:
  * Full name
  * New address (including city, street, house number)
  * Email
  * Moving date (or estimated date)

- For Both Services:
  * Full name
  * Both current and new addresses
  * Email
  * Moving date (or estimated date)

### 4. Details Verification
- System displays provided details for verification
- Header: "✅ אימות פרטים"
- User options:
  * "כן, הפרטים נכונים ✅" -> Proceeds to photo stage
  * "לא, צריך לתקן ❌" -> Returns to details collection with prompt to rewrite
  * Back to main menu
  * Talk to representative

### 5. Photo Requirement Stage
Header: "שליחת תמונות 📸"

Two possible paths:

#### Path A: Photo Request
- System requests photos/videos with specific instructions:
  * Focus on cabinets/closets with open doors
  * Kitchen storage areas
  * General home views
- System explains photos are for quote purposes only and won't be stored
- User can:
  * Send photos/videos -> Proceeds to scheduling
  * Choose to skip -> Proceeds to scheduling
  * Navigate to main menu
  * Request representative contact

#### Path B: Skip Photos
- User selects "מעדיפים לדלג" (prefer to skip)
- Proceeds directly to call scheduling

### 6. Call Scheduling
Header: "תיאום שיחת טלפון 📞"
1. Initial Scheduling:
   - System displays message: "כדי להשלים את התהליך, נשמח לקיים שיחה קצרה לתיאום ציפיות"
   - Presents dynamically generated time slots
   - Additional options:
     * Back to main menu
     * Talk to representative

2. After Slot Selection:
   - Sends confirmation message with selected time slot
   - Provides option to change slot: "שינוי מועד השיחה"
   - If change requested:
     * Re-calculates available time slots
     * Presents new options
   - Label management:
     * Removes: `bot_new_conversation`
     * Applies: `waiting_call_before_quote`

3. Error handling:
   - If slot generation fails, displays fallback message
   - Fallback includes basic confirmation and representative contact option

### 7. Flow Completion
Final confirmation message includes:
1. Chosen time slot confirmation
2. Brief message about upcoming call
3. Option to change slot time
4. Label status:
   - `bot_new_conversation`: Removed
   - `waiting_call_before_quote`: Applied

## State Machine
The conversation follows these states with specific transitions:

1. `awaiting_packing_choice`
   - Valid transitions: awaiting_customer_details, error
   - Triggers: service selection button click

2. `awaiting_customer_details`
   - Valid transitions: awaiting_verification, error
   - Triggers: text message with details

3. `awaiting_verification`
   - Valid transitions: awaiting_photos, awaiting_customer_details
   - Triggers: verification button click

4. `awaiting_photos`
   - Valid transitions: awaiting_slot_selection
   - Triggers: photo/video upload or skip option

5. `awaiting_slot_selection`
   - Valid transitions: completed, awaiting_slot_selection (if change requested), error
   - Triggers: time slot selection

6. `completed`
   - Can return to awaiting_slot_selection if slot change requested
   - Otherwise, final state

## Error Handling
1. Invalid Input Handling:
   - Each state has specific validation
   - Returns to current state with error message
   - Maintains context and user progress

2. Scheduling Failures:
   - Fallback message with header "✅ הפניה התקבלה"
   - Basic confirmation: "תודה על פנייתך! נציג מהצוות שלנו יצור איתך קשר בהקדם"
   - Provides navigation options

3. Navigation Safety:
   - All states support return to main menu
   - All states support requesting representative contact
   - Preserves service type across navigation

## Navigation Options
Available throughout the flow:
- Return to main menu: Resets conversation to initial state
- Talk to representative: 
  * Transfers conversation to human support
  * Removes `bot_new_conversation` label
  * Applies `waiting_for_support_urgent` label
  * Sends support notification message
- Back option: Context-aware, returns to previous relevant state
- State-specific options as detailed in each stage