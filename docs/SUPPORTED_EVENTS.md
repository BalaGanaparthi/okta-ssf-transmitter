# Okta-Supported Event Types (6 Total)

## ✅ Only Events Okta Officially Supports

Based on Okta's SSF API documentation, the transmitter now implements **only the 6 event types** that Okta actually supports as an SSF receiver.

---

## 📊 Supported Events

### 1. **Device Risk Change** (Okta)
**URI:** `https://schemas.okta.com/secevent/okta/event-type/device-risk-change`

**Description:** Signal changes in device risk level

**Required Fields:**
- `current_level` (dropdown: low/medium/high)
- `previous_level` (dropdown: low/medium/high)

**Optional Fields:**
- `event_timestamp` (datetime picker → Unix timestamp)
- `initiating_entity` (dropdown: admin/system/user)
- `reason_admin` (text)
- `reason_user` (text)

**Example Use Case:** Trusted device becomes suspicious

---

### 2. **IP Change** (Okta)
**URI:** `https://schemas.okta.com/secevent/okta/event-type/ip-change`

**Description:** User IP address has changed

**Required Fields:**
- `current_ip` (text input: IP address)

**Optional Fields:**
- `previous_ip` (text input: IP address)
- `event_timestamp` (datetime picker → Unix timestamp)
- `initiating_entity` (dropdown: admin/system/user)
- `reason_admin` (text)

**Example Use Case:** User logged in from new location

---

### 3. **User Risk Change** (Okta)
**URI:** `https://schemas.okta.com/secevent/okta/event-type/user-risk-change`

**Description:** Signal changes in user risk level

**Required Fields:**
- `current_level` (dropdown: low/medium/high)
- `previous_level` (dropdown: low/medium/high)

**Optional Fields:**
- `event_timestamp` (datetime picker → Unix timestamp)
- `initiating_entity` (dropdown: admin/system/user)
- `reason_admin` (text)
- `reason_user` (text)

**Example Use Case:** User account becomes high risk due to impossible travel

---

### 4. **Device Compliance Change** (CAEP)
**URI:** `https://schemas.openid.net/secevent/caep/event-type/device-compliance-change`

**Description:** Device compliance status has changed

**Required Fields:**
- `current_status` (dropdown: compliant/not_compliant)

**Optional Fields:**
- `previous_status` (dropdown: compliant/not_compliant)
- `event_timestamp` (datetime picker → Unix timestamp)
- `reason_admin` (text)

**Example Use Case:** Device no longer meets security requirements

---

### 5. **Session Revoked** (CAEP)
**URI:** `https://schemas.openid.net/secevent/caep/event-type/session-revoked`

**Description:** User session has been revoked

**Required Fields:** None (all optional)

**Optional Fields:**
- `session_id` (text: session identifier)
- `event_timestamp` (datetime picker → Unix timestamp)
- `initiating_entity` (dropdown: admin/system/user)
- `reason_admin` (text)
- `reason_user` (text)

**Example Use Case:** Force logout due to security event

---

### 6. **Identifier Changed** (RISC)
**URI:** `https://schemas.openid.net/secevent/risc/event-type/identifier-changed`

**Description:** User identifier has been modified

**Required Fields:** None (all optional)

**Optional Fields:**
- `new-value` (text: new email or phone)
- `event_timestamp` (datetime picker → Unix timestamp)

**Example Use Case:** User changed email address

---

## 🎨 UI Behavior by Event

### Events with Risk Level Dropdowns:
- **Device Risk Change**
- **User Risk Change**

**UI Shows:**
```
Current Risk Level *: [Low/Medium/High ▼]
Previous Risk Level *: [Low/Medium/High ▼]
```

### Event with IP Address Fields:
- **IP Change**

**UI Shows:**
```
Current IP Address *: [192.168.1.100]
Previous IP Address: [10.0.0.50]
```

### Event with Compliance Dropdowns:
- **Device Compliance Change**

**UI Shows:**
```
Current Compliance Status *: [Compliant/Not Compliant ▼]
Previous Compliance Status: [Compliant/Not Compliant ▼]
```

### Event with Session Field:
- **Session Revoked**

**UI Shows:**
```
Session ID: [session_abc123xyz]
```

### Event with Identifier Field:
- **Identifier Changed**

**UI Shows:**
```
New Identifier Value: [new-email@example.com]
```

---

## 🔧 What Was Removed

### Removed Unsupported Events (9):
- ❌ CREDENTIAL_CHANGE_REQUIRED
- ❌ CREDENTIAL_COMPROMISE
- ❌ ACCOUNT_DISABLED
- ❌ ACCOUNT_ENABLED
- ❌ ACCOUNT_PURGED
- ❌ IDENTIFIER_RECYCLED
- ❌ RECOVERY_ACTIVATED
- ❌ RECOVERY_INFORMATION_CHANGED
- ❌ OPT_IN, OPT_OUT_INITIATED, OPT_OUT_CANCELLED, OPT_OUT_EFFECTIVE

**Reason:** Okta documentation only lists 6 supported event types

---

## ✅ Verification

### Test Results:
```
======================== 13 passed, 1 warning in 0.46s =========================

✅ All 6 event types present in EVENT_TYPES
✅ All field schemas defined
✅ All tests updated and passing
✅ UI updated to show 6 events
```

### Event Count Verification:
```python
from src.ssf_transmitter.core import EVENT_TYPES
len(EVENT_TYPES)  # Returns: 6 ✅
```

---

## 🎯 Categories

Events organized into 3 categories:

### Okta Events (3)
- Device Risk Change
- IP Change
- User Risk Change

### CAEP Events (2)
- Device Compliance Change
- Session Revoked

### RISC Events (1)
- Identifier Changed

---

## 🚀 After Deployment

### Dropdown Will Show:

```
Select an event type...
├─ CAEP Events
│  ├─ Device Compliance Change
│  └─ Session Revoked
├─ Okta Events
│  ├─ Device Risk Change
│  ├─ IP Change
│  └─ User Risk Change
└─ RISC Events
   └─ Identifier Changed
```

---

## 📋 Quick Reference

| Event | Category | Required Fields | Use Case |
|-------|----------|----------------|----------|
| Device Risk Change | Okta | current_level, previous_level | Device becomes suspicious |
| IP Change | Okta | current_ip | User from new location |
| User Risk Change | Okta | current_level, previous_level | User risk increases |
| Device Compliance Change | CAEP | current_status | Device non-compliant |
| Session Revoked | CAEP | None | Force logout |
| Identifier Changed | RISC | None | Email/phone changed |

---

## 🎉 Summary

**Before:** 15+ events (many unsupported)

**After:** 6 events (all officially supported by Okta)

**Result:** Clean, focused, production-ready

**Status:** Ready to deploy ✅

---

**All 6 events will work correctly with Okta!** 🚀
