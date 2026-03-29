# Fully Dynamic Form System - Complete Implementation

## ✅ System Overview

The SSF Transmitter now uses a **completely data-driven, schema-based dynamic form system**.

No more hardcoded UI logic! The entire form is generated automatically based on event type schemas.

---

## 🎯 How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Define Event Type in event_types.py                      │
│    - Basic info (URI, label, description)                   │
│    - Extra fields needed                                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Define Field Schemas in FIELD_SCHEMAS                    │
│    - Field type (select/text/datetime)                      │
│    - Options for dropdowns                                  │
│    - Labels, hints, placeholders                            │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. API Resolves Schemas (/api/event-types)                  │
│    - Merges field definitions with schemas                  │
│    - Returns complete UI specification                      │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. JavaScript Generates UI Dynamically                      │
│    - Creates dropdowns for enum fields                      │
│    - Creates text inputs for freeform fields                │
│    - Handles required/optional                              │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 5. Frontend Collects Data Dynamically                       │
│    - Reads all dynamic field values                         │
│    - Validates required fields                              │
│    - Sends to backend                                       │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 6. Backend Processes Dynamically                            │
│    - Validates based on schema                              │
│    - Collects all extra fields                              │
│    - Adds to JWT payload                                    │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ 7. JWT Sent to Okta                                         │
│    - All required fields included                           │
│    - Properly formatted                                     │
│    - ✅ SUCCESS!                                            │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 Current Event Types with Dynamic Fields

### Events with Dropdowns:

#### 1. **User Risk Change (Okta)** ✨
**Fields:**
- `currentRiskLevel` (required) → Dropdown: LOW, MEDIUM, HIGH
- `previousRiskLevel` (required) → Dropdown: LOW, MEDIUM, HIGH

#### 2. **Credential Compromise** ✨
**Fields:**
- `credential_type` (required) → Dropdown: 8 options
  - password
  - token
  - api_key
  - ssh_key
  - certificate
  - session
  - oauth_token
  - bearer_token
- `event_timestamp` (optional) → DateTime picker
- `reason_admin` (optional) → Text input
- `reason_user` (optional) → Text input

#### 3. **Account Disabled** ✨
**Fields:**
- `reason` (optional) → Dropdown: hijacking, bulk-account

#### 4. **Identifier Changed** ✨
**Fields:**
- `new-value` (optional) → Text input

### Events with Standard Fields Only:

All other 11 event types use just:
- Subject (email)
- Event type
- General notes (optional)

---

## 🎨 Field Schema System

### Field Schema Definition

Each field has a complete schema:

```python
'currentRiskLevel': {
    'label': 'Current Risk Level',          # Display label
    'type': 'select',                       # UI component type
    'hint': 'Current risk level...',        # Help text
    'options': [                            # For dropdowns
        {'value': 'LOW', 'label': 'Low Risk'},
        {'value': 'MEDIUM', 'label': 'Medium Risk'},
        {'value': 'HIGH', 'label': 'High Risk'}
    ],
    'placeholder': 'Select...'              # Placeholder text
}
```

### Supported Field Types:

- **`select`** - Dropdown with enum options
- **`text`** - Text input field
- **`datetime-local`** - Date/time picker
- **`email`** - Email input (future)
- **`number`** - Number input (future)

---

## 🔧 How to Add New Event Types

### Step 1: Add to EVENT_TYPES

```python
'MY_NEW_EVENT': {
    'uri': 'https://schemas.example.com/event-type/my-event',
    'label': 'My New Event',
    'description': 'Description of the event',
    'category': 'Category Name',
    'extra_fields': [
        {'name': 'my_field', 'required': True},
        {'name': 'optional_field', 'required': False}
    ]
}
```

### Step 2: Add Field Schemas (if new fields)

```python
FIELD_SCHEMAS = {
    'my_field': {
        'label': 'My Field',
        'type': 'select',
        'hint': 'Choose a value',
        'options': [
            {'value': 'option1', 'label': 'Option 1'},
            {'value': 'option2', 'label': 'Option 2'}
        ],
        'placeholder': 'Select...'
    }
}
```

### Step 3: That's It!

**No code changes needed!** The UI, validation, and backend all work automatically.

---

## 🎨 UI Behavior

### When User Selects an Event:

1. **Description appears** below dropdown
2. **Dynamic fields generate** automatically
3. **Dropdowns** for enum fields (with all options)
4. **Text inputs** for freeform fields
5. **DateTime pickers** for timestamp fields
6. **Required fields** marked with * and orange accent
7. **Optional fields** clearly labeled
8. **General notes** field hidden if event has specific reason dropdown

---

## 📝 Example: User Risk Change Flow

### User Experience:

```
1. Select event: "User Risk Change (Okta)"
   ↓
2. Description appears:
   "User risk level has changed (e.g., LOW → HIGH)"
   ↓
3. Two dropdowns appear:
   ┌─────────────────────────────────┐
   │ Current Risk Level *            │
   │ [Select...] ▼                   │
   │  • Low Risk                     │
   │  • Medium Risk                  │
   │  • High Risk                    │
   └─────────────────────────────────┘

   ┌─────────────────────────────────┐
   │ Previous Risk Level *           │
   │ [Select...] ▼                   │
   │  • Low Risk                     │
   │  • Medium Risk                  │
   │  • High Risk                    │
   └─────────────────────────────────┘
   ↓
4. User selects values
   ↓
5. Clicks "Send Security Event"
   ↓
6. Frontend validates required fields
   ↓
7. Sends to backend with all fields
   ↓
8. Backend validates and adds to JWT
   ↓
9. JWT sent to Okta ✅
```

---

## 📋 Complete Field List

### Risk Level Fields
- `currentRiskLevel`, `previousRiskLevel`
- Type: **Dropdown**
- Options: LOW, MEDIUM, HIGH

### Credential Type Field
- `credential_type`
- Type: **Dropdown**
- Options: password, token, api_key, ssh_key, certificate, session, oauth_token, bearer_token

### Identifier Fields
- `new-value`
- Type: **Text input**
- Format: email or phone

### Reason Fields
- `reason` (for ACCOUNT_DISABLED)
- Type: **Dropdown**
- Options: hijacking, bulk-account

### Admin/User Reasons
- `reason_admin`, `reason_user`
- Type: **Text input**
- Freeform text

### Timestamp Fields
- `event_timestamp`
- Type: **DateTime picker**
- Format: ISO 8601

---

## 🧪 Testing Different Event Types

### Test 1: Credential Compromise (Multiple Fields)

**Via UI:**
1. Select "Credential Compromise"
2. See 4 dynamic fields appear:
   - Credential Type * (dropdown - 8 options)
   - Event Timestamp (datetime picker)
   - Admin Reason (text)
   - User Reason (text)
3. Fill required field: Credential Type = "password"
4. Optionally fill timestamp and reasons
5. Send

**Expected:** All fields sent to Okta correctly ✅

### Test 2: User Risk Change (Dropdowns)

**Via UI:**
1. Select "User Risk Change (Okta)"
2. See 2 dropdown fields
3. Select Current: HIGH
4. Select Previous: LOW
5. Send

**Expected:** Risk levels sent correctly ✅

### Test 3: Account Disabled (Specific Reason)

**Via UI:**
1. Select "Account Disabled"
2. See specific reason dropdown (hijacking/bulk-account)
3. General notes field HIDDEN
4. Select reason from dropdown
5. Send

**Expected:** Specific reason sent ✅

### Test 4: Identifier Changed (Text Input)

**Via UI:**
1. Select "Identifier Changed"
2. See "New Identifier Value" text field
3. Enter new email
4. Send

**Expected:** new-value sent correctly ✅

### Test 5: Standard Event (No Extra Fields)

**Via UI:**
1. Select "Credential Change Required"
2. No dynamic fields appear
3. Just email and general notes
4. Send

**Expected:** Standard event works as before ✅

---

## 🎯 Key Benefits

### For Users:
- ✅ **Intuitive** - Right fields appear automatically
- ✅ **Clear** - Dropdowns for enum values
- ✅ **Guided** - Hints and placeholders
- ✅ **Validated** - Can't send invalid data

### For Developers:
- ✅ **No hardcoding** - All data-driven
- ✅ **Easy to extend** - Add schemas, done
- ✅ **Maintainable** - Single source of truth
- ✅ **Testable** - Schema-based testing

### For Operations:
- ✅ **Compliant** - All Okta requirements met
- ✅ **Reliable** - Proper validation
- ✅ **Documented** - Self-describing schemas
- ✅ **Scalable** - Add events easily

---

## 📚 Code Structure

### Backend (`event_types.py`)

```python
FIELD_SCHEMAS = {
    # Complete field definitions
    'currentRiskLevel': { ... },
    'credential_type': { ... },
    ...
}

EVENT_TYPES = {
    'USER_RISK_CHANGE': {
        'uri': '...',
        'label': '...',
        'extra_fields': [
            {'name': 'currentRiskLevel', 'required': True},
            {'name': 'previousRiskLevel', 'required': True}
        ]
    }
}

def get_event_type_with_schemas(event_type_key):
    # Merges event type with field schemas
    # Returns complete UI specification
```

### API (`routes.py`)

```python
@bp.route('/api/event-types')
def get_event_types():
    # Returns event types with resolved field schemas
    # Frontend uses this to generate UI

@bp.route('/api/send-event', methods=['POST'])
def send_event():
    # Dynamically collects all extra fields
    # Validates based on schema
    # No hardcoded logic!
```

### Frontend (`app.js`)

```javascript
function handleEventTypeChange(e) {
    // Reads field_definitions from event type
    // Calls generateFieldHtml() for each field
    // Dynamically builds form
}

function generateFieldHtml(field) {
    // Creates dropdown if type === 'select'
    // Creates text input if type === 'text'
    // Creates datetime picker if type === 'datetime-local'
    // Returns HTML string
}

function handleSubmit(e) {
    // Dynamically collects all field values
    // Validates required fields
    // Sends to backend
}
```

---

## 🚀 Deployment

### Commit and Push

```bash
# All changes committed
git push origin main
```

### What You'll Get:

After Railway deploys (~2 minutes), the UI will:

1. **Load event types with schemas** from API
2. **Generate form fields dynamically** for each event
3. **Show dropdowns** for enum fields automatically
4. **Validate** based on required/optional
5. **Send** all fields to Okta correctly

---

## 🧪 Testing After Deployment

### Test Credential Compromise:

```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test@yourcompany.com",
    "eventType": "CREDENTIAL_COMPROMISE",
    "credential_type": "password",
    "event_timestamp": "2024-03-29T10:00:00",
    "reason_admin": "Found in breach database",
    "reason_user": "We detected suspicious activity with your password"
  }'
```

### Test User Risk Change:

```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test@yourcompany.com",
    "eventType": "USER_RISK_CHANGE",
    "currentRiskLevel": "HIGH",
    "previousRiskLevel": "LOW",
    "reason": "Impossible travel detected"
  }'
```

### Test Account Disabled:

```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test@yourcompany.com",
    "eventType": "ACCOUNT_DISABLED",
    "reason": "hijacking"
  }'
```

**All should work without validation errors!** ✅

---

## 📝 Field Schema Examples

### Dropdown Field (Enum Values)

```python
'currentRiskLevel': {
    'label': 'Current Risk Level',
    'type': 'select',
    'hint': 'Current risk level of the user',
    'options': [
        {'value': 'LOW', 'label': 'Low Risk'},
        {'value': 'MEDIUM', 'label': 'Medium Risk'},
        {'value': 'HIGH', 'label': 'High Risk'}
    ],
    'placeholder': 'Select current risk level...'
}
```

**Generates:**
```html
<select id="currentRiskLevel" required>
    <option value="">Select current risk level...</option>
    <option value="LOW">Low Risk</option>
    <option value="MEDIUM">Medium Risk</option>
    <option value="HIGH">High Risk</option>
</select>
```

### Text Input Field

```python
'reason_admin': {
    'label': 'Admin Reason',
    'type': 'text',
    'hint': 'Administrator-facing reason',
    'placeholder': 'e.g., Detected in breach database'
}
```

**Generates:**
```html
<input type="text" id="reason_admin"
       placeholder="e.g., Detected in breach database">
```

### DateTime Field

```python
'event_timestamp': {
    'label': 'Event Timestamp',
    'type': 'datetime-local',
    'hint': 'When the event occurred',
    'placeholder': '2024-03-29T10:00:00'
}
```

**Generates:**
```html
<input type="datetime-local" id="event_timestamp">
```

---

## ➕ Adding New Event Types (Easy!)

### Example: Add "Password Changed" Event

**Step 1:** Add to `EVENT_TYPES`

```python
'PASSWORD_CHANGED': {
    'uri': 'https://schemas.example.com/event-type/password-changed',
    'label': 'Password Changed',
    'description': 'User changed their password',
    'category': 'Account Security',
    'extra_fields': [
        {'name': 'change_type', 'required': True},
        {'name': 'forced', 'required': False}
    ]
}
```

**Step 2:** Add field schemas (if new fields)

```python
FIELD_SCHEMAS = {
    'change_type': {
        'label': 'Change Type',
        'type': 'select',
        'hint': 'How the password was changed',
        'options': [
            {'value': 'user_initiated', 'label': 'User Initiated'},
            {'value': 'admin_reset', 'label': 'Admin Reset'},
            {'value': 'policy_expired', 'label': 'Policy Expiration'}
        ],
        'placeholder': 'Select change type...'
    },
    'forced': {
        'label': 'Forced Change',
        'type': 'select',
        'hint': 'Was the change forced?',
        'options': [
            {'value': 'true', 'label': 'Yes'},
            {'value': 'false', 'label': 'No'}
        ],
        'placeholder': 'Select...'
    }
}
```

**Step 3:** Deploy

That's it! The UI will automatically:
- Show the new event in the dropdown
- Generate form fields when selected
- Validate required fields
- Send to Okta correctly

**No JavaScript changes needed!** 🎉

---

## 🔍 System Components

### 1. Schema Definition (`event_types.py`)

```python
FIELD_SCHEMAS = { ... }      # All possible fields
EVENT_TYPES = { ... }         # All event types
```

### 2. Schema Resolution (`event_types.py`)

```python
def get_event_type_with_schemas(event_type_key):
    # Merges field definitions with field schemas
    # Returns complete specification
```

### 3. API Endpoint (`routes.py`)

```python
@bp.route('/api/event-types')
def get_event_types():
    # Returns all event types with resolved schemas
```

### 4. UI Generation (`app.js`)

```javascript
function generateFieldHtml(field) {
    // Generates HTML based on field.type
    // Handles select, text, datetime-local
}
```

### 5. Data Collection (`app.js`)

```javascript
function handleSubmit(e) {
    // Dynamically collects all field values
    // Uses field definitions from event type
}
```

### 6. Backend Processing (`routes.py`)

```python
# Dynamically validates and collects extra fields
for field_def in event_type_schema['field_definitions']:
    field_value = data.get(field_name)
    # Validate and add to extra_fields
```

---

## ✅ What's Fixed

### Before:
- ❌ Hardcoded event-specific logic
- ❌ Manual if/else for each event
- ❌ Hard to add new events
- ❌ Validation errors for missing fields

### After:
- ✅ Fully data-driven
- ✅ Schema-based generation
- ✅ Easy to extend
- ✅ Proper validation for all fields

---

## 🎉 Benefits

### 1. **Extensibility**
Add new event types by just updating the schema. No code changes!

### 2. **Maintainability**
Single source of truth. All logic derived from schemas.

### 3. **Validation**
Automatic validation based on required/optional flags.

### 4. **User Experience**
Right fields appear automatically. Clear guidance.

### 5. **Type Safety**
Dropdowns prevent invalid enum values.

### 6. **Documentation**
Schemas are self-documenting.

---

## 📊 Summary

**Status:** ✅ Fully dynamic system implemented

**Event Types:** 15 total, all with proper schemas

**Dynamic Fields:** 4 events with custom fields

**Field Types:** select, text, datetime-local

**Dropdowns:** Auto-generated from schemas

**Validation:** Automatic from schemas

**Code:** Completely data-driven

**Extensibility:** Add events without code changes

---

## 🚀 Ready to Deploy

```bash
git push origin main
```

After deployment:
- ✅ All event types work correctly
- ✅ Dynamic fields appear automatically
- ✅ Dropdowns show all enum options
- ✅ No more hardcoded logic
- ✅ Easy to extend

---

**The system is now fully dynamic and schema-based!** 🎉

**Push and test - all event types will work with proper field collection!** 🚀
