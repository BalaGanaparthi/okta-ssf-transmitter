# SSF Event Types - Complete Guide

## Overview

The SSF Transmitter now supports **16 different security event types** based on the OpenID RISC (Risk and Incident Sharing and Coordination) profile plus Okta-specific events.

All events are organized into **6 categories** in the UI dropdown for easy selection.

---

## Event Types by Category

### 1. Account Security (5 Events)

#### ✅ Credential Change Required
**URI:** `https://schemas.openid.net/secevent/risc/event-type/account-credential-change-required`

**When to use:**
- Password compromised in data breach
- Weak password detected
- Suspicious credential usage
- Compliance requirement

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "CREDENTIAL_CHANGE_REQUIRED",
  "reason": "Password found in HaveIBeenPwned database"
}
```

#### 🔐 Credential Compromise
**URI:** `https://schemas.openid.net/secevent/risc/event-type/credential-compromise`

**When to use:**
- Confirmed credential theft
- Phishing attack successful
- Keylogger detected
- Credential stuffing attack

**Required fields:**
- `credential_type`: Type of credential (e.g., "password", "token")

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "CREDENTIAL_COMPROMISE",
  "credential_type": "password",
  "reason": "Phishing attack confirmed"
}
```

#### 🚫 Account Disabled
**URI:** `https://schemas.openid.net/secevent/risc/event-type/account-disabled`

**When to use:**
- Suspicious activity detected
- Multiple failed login attempts
- Security policy violation
- Temporary account lock

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "ACCOUNT_DISABLED",
  "reason": "10 failed login attempts from multiple IPs"
}
```

#### ✅ Account Enabled
**URI:** `https://schemas.openid.net/secevent/risc/event-type/account-enabled`

**When to use:**
- Investigation completed - user cleared
- False positive resolved
- Account appeal approved
- Temporary lock expired

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "ACCOUNT_ENABLED",
  "reason": "Investigation completed - activity verified as legitimate"
}
```

#### 🗑️ Account Purged
**URI:** `https://schemas.openid.net/secevent/risc/event-type/account-purged`

**When to use:**
- Account permanently deleted
- GDPR data deletion request
- Account closure by user
- Compliance requirement

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "ACCOUNT_PURGED",
  "reason": "User requested account deletion (GDPR)"
}
```

---

### 2. Identifier Management (2 Events)

#### 🔄 Identifier Changed
**URI:** `https://schemas.openid.net/secevent/risc/event-type/identifier-changed`

**When to use:**
- Email address changed
- Phone number updated
- Username modified
- User profile update

**Optional fields:**
- `new-value`: The new identifier value

**Example:**
```json
{
  "subject": "old-email@example.com",
  "eventType": "IDENTIFIER_CHANGED",
  "new-value": "new-email@example.com",
  "reason": "User updated email address"
}
```

#### ♻️ Identifier Recycled
**URI:** `https://schemas.openid.net/secevent/risc/event-type/identifier-recycled`

**When to use:**
- Email address reassigned to new user
- Phone number recycled by carrier
- Username reused after deletion
- Identifier ownership changed

**Example:**
```json
{
  "subject": "recycled@example.com",
  "eventType": "IDENTIFIER_RECYCLED",
  "reason": "Email address reassigned to new account after 90 days"
}
```

---

### 3. Recovery (2 Events)

#### 🔓 Recovery Activated
**URI:** `https://schemas.openid.net/secevent/risc/event-type/recovery-activated`

**When to use:**
- Password reset requested
- Account recovery started
- 2FA recovery initiated
- Forgot password flow

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "RECOVERY_ACTIVATED",
  "reason": "User initiated password reset"
}
```

#### 📧 Recovery Information Changed
**URI:** `https://schemas.openid.net/secevent/risc/event-type/recovery-information-changed`

**When to use:**
- Backup email changed
- Recovery phone updated
- Security questions modified
- Recovery method added/removed

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "RECOVERY_INFORMATION_CHANGED",
  "reason": "User added backup email address"
}
```

---

### 4. Opt-In/Out (4 Events)

#### ✔️ Opt In
**URI:** `https://schemas.openid.net/secevent/risc/event-type/opt-in`

**When to use:**
- User consents to RISC sharing
- Privacy settings updated
- Terms accepted
- Sharing enabled

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "OPT_IN",
  "reason": "User consented to security event sharing"
}
```

#### ⏸️ Opt Out Initiated
**URI:** `https://schemas.openid.net/secevent/risc/event-type/opt-out-initiated`

**When to use:**
- User requests to opt out
- Privacy preference change
- Sharing disabled (pending)

**Note:** Events continue during grace period

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "OPT_OUT_INITIATED",
  "reason": "User requested opt-out via privacy settings"
}
```

#### ↩️ Opt Out Cancelled
**URI:** `https://schemas.openid.net/secevent/risc/event-type/opt-out-cancelled`

**When to use:**
- User cancels opt-out request
- Changed mind during grace period
- Sharing re-enabled

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "OPT_OUT_CANCELLED",
  "reason": "User cancelled opt-out request"
}
```

#### ⛔ Opt Out Effective
**URI:** `https://schemas.openid.net/secevent/risc/event-type/opt-out-effective`

**When to use:**
- Opt-out grace period expired
- Sharing now disabled
- Final opt-out confirmation

**Note:** No more events will be sent after this

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "OPT_OUT_EFFECTIVE",
  "reason": "Opt-out grace period completed"
}
```

---

### 5. Session Management (1 Event)

#### 🔒 Sessions Revoked ⚠️ **DEPRECATED**
**URI:** `https://schemas.openid.net/secevent/risc/event-type/sessions-revoked`

**When to use:**
- All user sessions terminated
- Global logout triggered
- Security breach response

**Note:** This event type is deprecated. Use CAEP (Continuous Access Evaluation Profile) instead for session management.

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "SESSIONS_REVOKED",
  "reason": "User clicked 'Log out all devices'"
}
```

---

### 6. Okta Specific (1 Event)

#### ⚠️ User Risk Change
**URI:** `https://schemas.okta.com/secevent/okta/event-type/user-risk-change`

**When to use:**
- Risk score changed
- Threat level increased/decreased
- Risk assessment updated
- Anomaly detected

**Required fields:**
- `current-level`: Current risk level (e.g., "HIGH", "MEDIUM", "LOW")

**Optional fields:**
- `previous-level`: Previous risk level
- `reason`: Why risk changed

**Example:**
```json
{
  "subject": "user@example.com",
  "eventType": "USER_RISK_CHANGE",
  "current-level": "HIGH",
  "previous-level": "LOW",
  "reason": "Login from unusual location with impossible travel"
}
```

---

## Usage in the UI

### The Dropdown

Events are organized by category in the dropdown:

```
Select an event type...
├─ Account Security
│  ├─ Account Disabled
│  ├─ Account Enabled
│  ├─ Account Purged
│  ├─ Credential Change Required
│  └─ Credential Compromise
├─ Identifier Management
│  ├─ Identifier Changed
│  └─ Identifier Recycled
├─ Opt-In/Out
│  ├─ Opt In
│  ├─ Opt Out Cancelled
│  ├─ Opt Out Effective
│  └─ Opt Out Initiated
├─ Okta Specific
│  └─ User Risk Change (Okta)
├─ Recovery
│  ├─ Recovery Activated
│  └─ Recovery Information Changed
└─ Session Management
   └─ Sessions Revoked (Deprecated) ⚠️
```

### When You Select an Event

1. **Description appears** - Explains what the event means
2. **Required fields** - Form updates if special fields needed
3. **Category shown** - Visual organization

---

## API Usage

### Via Web UI
1. Select user email
2. Choose event type from dropdown
3. Add optional reason
4. Click "Send Security Event"

### Via cURL

```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "user@example.com",
    "eventType": "CREDENTIAL_CHANGE_REQUIRED",
    "reason": "Password compromised in breach"
  }'
```

### Via Postman

```json
POST https://your-app.railway.app/api/send-event
Content-Type: application/json

{
  "subject": "user@example.com",
  "eventType": "ACCOUNT_DISABLED",
  "reason": "Multiple failed login attempts"
}
```

---

## Common Use Cases

### Security Breach Response
1. **CREDENTIAL_COMPROMISE** - Report the breach
2. **CREDENTIAL_CHANGE_REQUIRED** - Force password reset
3. **SESSIONS_REVOKED** - Log out all devices

### Suspicious Activity
1. **ACCOUNT_DISABLED** - Temporarily lock account
2. **USER_RISK_CHANGE** - Update risk level
3. **RECOVERY_ACTIVATED** - Monitor for recovery attempts

### Account Lifecycle
1. **OPT_IN** - User consents
2. **IDENTIFIER_CHANGED** - Email updated
3. **ACCOUNT_PURGED** - Account deleted

### False Positive
1. **ACCOUNT_ENABLED** - Unlock account
2. **USER_RISK_CHANGE** - Lower risk level

---

## Event Type Selection Guide

### High Severity Events
- **CREDENTIAL_COMPROMISE** - Confirmed breach
- **ACCOUNT_DISABLED** - Security threat
- **USER_RISK_CHANGE** (HIGH) - Critical risk

### Medium Severity Events
- **CREDENTIAL_CHANGE_REQUIRED** - Precautionary
- **SESSIONS_REVOKED** - Preventative
- **ACCOUNT_PURGED** - Permanent action

### Low Severity Events
- **IDENTIFIER_CHANGED** - Informational
- **RECOVERY_INFORMATION_CHANGED** - Profile update
- **OPT_IN/OUT** - Privacy preference

### Informational Events
- **ACCOUNT_ENABLED** - Status change
- **RECOVERY_ACTIVATED** - User action
- **OPT_OUT_CANCELLED** - Preference change

---

## Best Practices

### 1. Always Provide Reason
While optional, reasons help:
- Debugging
- Audit trails
- User communication
- Compliance

### 2. Use Correct Event Type
Don't use:
- **ACCOUNT_DISABLED** for voluntary deletions (use **ACCOUNT_PURGED**)
- **CREDENTIAL_CHANGE_REQUIRED** for confirmed breaches (use **CREDENTIAL_COMPROMISE**)

### 3. Verify User Exists
All events require the user to exist in Okta. Test with:
```bash
curl https://your-org.okta.com/api/v1/users/user@example.com \
  -H "Authorization: SSWS YOUR_TOKEN"
```

### 4. Monitor Okta Logs
Check **Reports → System Log** after sending events to verify receipt.

### 5. Test in Non-Production First
Always test new event types with test users before production use.

---

## Troubleshooting

### Event Not Appearing in Okta
1. **Check user exists** in Okta
2. **Verify provider registered** with correct JWKS
3. **Wait 1-2 minutes** for processing
4. **Check System Log** with filters removed

### Validation Error
1. **Check required fields** for event type
2. **Verify event type key** is correct
3. **Check subject format** (must be email)

### Signature Error
1. **Re-register provider** with current JWKS
2. **Verify keys** using `/api/verify-keys`
3. **Wait for Okta** to refresh JWKS cache

---

## Quick Reference

| Event | Category | Severity | Common Use |
|-------|----------|----------|------------|
| CREDENTIAL_CHANGE_REQUIRED | Account Security | Medium | Data breach response |
| CREDENTIAL_COMPROMISE | Account Security | High | Confirmed attack |
| ACCOUNT_DISABLED | Account Security | High | Block suspicious user |
| ACCOUNT_ENABLED | Account Security | Low | Reinstate user |
| ACCOUNT_PURGED | Account Security | Medium | Delete account |
| IDENTIFIER_CHANGED | Identifier | Low | Email updated |
| IDENTIFIER_RECYCLED | Identifier | Medium | Email reassigned |
| RECOVERY_ACTIVATED | Recovery | Low | Password reset |
| RECOVERY_INFORMATION_CHANGED | Recovery | Low | Backup email added |
| OPT_IN | Opt-In/Out | Low | User consent |
| OPT_OUT_INITIATED | Opt-In/Out | Low | Privacy request |
| OPT_OUT_CANCELLED | Opt-In/Out | Low | Changed mind |
| OPT_OUT_EFFECTIVE | Opt-In/Out | Medium | Stop sharing |
| SESSIONS_REVOKED | Session | Medium | Global logout |
| USER_RISK_CHANGE | Okta | Variable | Risk assessment |

---

## References

- [OpenID RISC Specification](https://openid.net/specs/openid-risc-profile-specification-1_0.html)
- [Okta SSF Documentation](https://developer.okta.com/docs/guides/configure-ssf-receiver/)
- [RFC 8417 - Security Event Tokens](https://datatracker.ietf.org/doc/html/rfc8417)

---

**Updated:** March 29, 2026
**Version:** 2.0 - Full RISC + Okta support
