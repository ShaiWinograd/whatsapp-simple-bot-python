# Organization Service Flow

## Overview
The Organization service helps users get professional organization and arrangement services for their home. The service follows a streamlined flow to collect necessary information and schedule a consultation call.

## Flow States

### 1. Details Collection (awaiting_customer_details)
- User provides:
  - Full name
  - Address (city, street, and house number)
  - Email address
- Navigation options:
  - Back to main menu
  - Talk to representative

### 2. Details Verification (awaiting_verification)
- Shows collected details to user
- User confirms if details are correct:
  - Yes - proceed to slot selection
  - No - return to details collection
- Navigation options:
  - Back to main menu
  - Talk to representative

### 3. Call Scheduling (awaiting_slot_selection)
- Shows available time slots for consultation call
- User selects preferred time slot
- Options to:
  - Change selected time
  - Back to main menu
  - Talk to representative

### 4. Completion
- Confirmation of selected time slot
- End of conversation flow

## Navigation
- All stages include standard navigation buttons:
  - Back to main menu
  - Talk to representative

## Error Handling
- Invalid inputs result in appropriate error messages
- Users can always navigate back or request support
- Validation of minimum details length
- Fallback message if slot scheduling fails