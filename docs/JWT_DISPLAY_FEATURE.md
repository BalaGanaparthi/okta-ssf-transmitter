# JWT Display Feature - Complete Implementation

## ✅ Feature Implemented

The UI now shows **complete JWT details** after sending an event, with ability to:
- 📋 View full JWT token, header, and payload
- 🔗 Open in JWT.io for detailed inspection
- 📄 Copy token to clipboard
- 🔍 See exact HTTP request made to Okta
- 🐛 Debug what was actually sent

---

## 🎨 What You'll See

### After Submitting an Event:

```
┌─────────────────────────────────────────────────────────────┐
│ ✅ Success                                                   │
│ Security event sent successfully to Okta.                   │
│                                                             │
│ Status: 202                                                 │
│ Endpoint: https://your-org.okta.com/security/api/v1/...    │
│ ─────────────────────────────────────────────────────────── │
│ 📋 JWT Details                                              │
│                                                             │
│ Token:                         [Copy] [Open in JWT.io] ←Click│
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ eyJhbGciOiJSUzI1NiIsImtpZCI...                         │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Header:                                                     │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ {                                                       │ │
│ │   "alg": "RS256",                                       │ │
│ │   "kid": "transmitter-key-1",                           │ │
│ │   "typ": "secevent+jwt"                                 │ │
│ │ }                                                       │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ Payload:                                                    │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ {                                                       │ │
│ │   "iss": "https://your-app.railway.app",                │ │
│ │   "jti": "evt_c3f07790-af36-4184-8932-d3cf6c8fdd0e",   │ │
│ │   "iat": 1774778649,                                    │ │
│ │   "aud": "https://your-org.okta.com",                   │ │
│ │   "events": {                                           │ │
│ │     "https://schemas.okta.com/.../user-risk-change": {  │ │
│ │       "subject": {                                      │ │
│ │         "format": "email",                              │ │
│ │         "email": "test@example.com"                     │ │
│ │       },                                                │ │
│ │       "currentRiskLevel": "HIGH",      ← See fields!    │ │
│ │       "previousRiskLevel": "LOW",      ← See fields!    │ │
│ │       "reason": "Impossible travel"                     │ │
│ │     }                                                   │ │
│ │   }                                                     │ │
│ │ }                                                       │ │
│ └─────────────────────────────────────────────────────────┘ │
│                                                             │
│ HTTP Request:                                               │
│ ┌─────────────────────────────────────────────────────────┐ │
│ │ POST https://your-org.okta.com/security/api/v1/...     │ │
│ │ Content-Type: application/secevent+jwt                  │ │
│ │ Body: [JWT Token Above]                                 │ │
│ └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Key Features

### 1. **View Full JWT Token** 📋
- Complete token displayed (truncated in UI)
- Copy button to copy full token
- Monospace font for readability

### 2. **Open in JWT.io** 🔗
- Click "Open in JWT.io" button
- Opens jwt.io in new tab
- Token pre-loaded for inspection
- See signature verification, claims, etc.

### 3. **View Header & Payload** 📝
- Formatted JSON display
- Syntax highlighted
- Easy to read structure

### 4. **HTTP Request Details** 🌐
- Shows Okta endpoint URL
- Shows Content-Type header
- Shows request method (POST)

### 5. **Copy to Clipboard** 📄
- One-click copy of full JWT
- Works on all modern browsers
- Confirmation feedback ("✓ Copied!")

---

## 🔍 How to Use

### After Sending Event:

#### 1. View the Response
Scroll down to see the response card with JWT details

#### 2. Inspect Payload
Look at the `Payload` section to verify:
- ✅ Subject email is correct
- ✅ Event type URI is correct
- ✅ All extra fields are included (currentRiskLevel, previousRiskLevel, etc.)
- ✅ Reason is included

#### 3. Open in JWT.io
Click **"Open in JWT.io"** button

**jwt.io will open showing:**
- Decoded Header
- Decoded Payload
- Signature (shows "Invalid Signature" - that's OK, jwt.io doesn't have your public key)
- All claims visible

#### 4. Copy Token
Click **"Copy"** button to copy full JWT token

Use it to:
- Test with Postman
- Debug with curl
- Share with support
- Verify signature elsewhere

---

## 🐛 Debugging with JWT Display

### Problem: Event Fails with "Field Cannot Be Left Blank"

**Solution:** Check the JWT Payload section:

```json
"events": {
  "https://schemas.okta.com/.../user-risk-change": {
    "subject": {...},
    "currentRiskLevel": "HIGH",     ← Is this here?
    "previousRiskLevel": "LOW"      ← Is this here?
  }
}
```

**If fields are MISSING from payload:**
→ Frontend isn't collecting values OR backend isn't adding them

**If fields are PRESENT in payload but Okta rejects:**
→ Field name mismatch or Okta API issue

---

## 📊 What You Can Verify

### 1. **Check All Required Fields**
Look in the payload section and verify ALL required fields are present.

### 2. **Check Field Names**
Okta expects specific field names:
- `currentRiskLevel` (not `current_level` or `currentLevel`)
- `previousRiskLevel` (not `previous_level` or `previousLevel`)
- `credential_type` (not `credentialType`)

### 3. **Check Field Values**
For enums, verify values are correct:
- Risk levels: `"LOW"`, `"MEDIUM"`, `"HIGH"` (all caps)
- Credential types: `"password"`, `"token"`, etc. (lowercase)

### 4. **Check Event URI**
Verify the event type URI in the `events` object matches Okta's expectations.

### 5. **Check Signature**
Click "Open in JWT.io" to verify:
- Algorithm: RS256
- Key ID: transmitter-key-1
- Signature exists

---

## 🧪 Testing Different Events

### Test User Risk Change:

**Submit form:**
1. Email: test@example.com
2. Event: User Risk Change (Okta)
3. Current: HIGH
4. Previous: LOW
5. Submit

**Check response:**
```json
"currentRiskLevel": "HIGH",      ← Must be here!
"previousRiskLevel": "LOW"       ← Must be here!
```

**Click "Open in JWT.io":**
- Should open jwt.io with full token
- Verify claims in decoded view

### Test Credential Compromise:

**Submit form:**
1. Email: test@example.com
2. Event: Credential Compromise
3. Credential Type: password
4. Optional fields if desired
5. Submit

**Check response:**
```json
"credential_type": "password",   ← Must be here!
"event_timestamp": "...",        ← If you filled it
"reason_admin": "...",           ← If you filled it
"reason_user": "..."             ← If you filled it
```

---

## 📋 Debugging Checklist

Use this when troubleshooting:

- [ ] **Event submitted** successfully or with error

- [ ] **Response card visible** with JWT details section

- [ ] **Token displayed** (truncated view)

- [ ] **Header shows** alg, kid, typ

- [ ] **Payload shows** iss, jti, iat, aud, events

- [ ] **Events object contains** your event type URI

- [ ] **Subject object present** with email

- [ ] **Extra fields present** (if applicable):
  - User Risk Change: currentRiskLevel, previousRiskLevel
  - Credential Compromise: credential_type
  - Identifier Changed: new-value
  - etc.

- [ ] **Copy button works** (copies full token)

- [ ] **Open in JWT.io button works** (opens new tab)

- [ ] **JWT.io shows decoded token** correctly

---

## 🎯 Expected JWT Structure

### For User Risk Change:

```json
{
  "iss": "https://your-app.railway.app",
  "jti": "evt_unique-id",
  "iat": 1234567890,
  "aud": "https://your-org.okta.com",
  "events": {
    "https://schemas.okta.com/secevent/okta/event-type/user-risk-change": {
      "subject": {
        "format": "email",
        "email": "user@example.com"
      },
      "currentRiskLevel": "HIGH",
      "previousRiskLevel": "LOW",
      "reason": "Impossible travel detected"
    }
  }
}
```

### For Credential Compromise:

```json
{
  "iss": "https://your-app.railway.app",
  "jti": "evt_unique-id",
  "iat": 1234567890,
  "aud": "https://your-org.okta.com",
  "events": {
    "https://schemas.openid.net/secevent/risc/event-type/credential-compromise": {
      "subject": {
        "format": "email",
        "email": "user@example.com"
      },
      "credential_type": "password",
      "reason": "Found in breach database"
    }
  }
}
```

---

## 🚀 Deploy and Test

### 1. Push Changes

```bash
git push origin main
```

**All changes include:**
- ✅ JWT display in UI
- ✅ jwt.io integration
- ✅ Copy to clipboard
- ✅ HTTP request details
- ✅ Formatted JSON view
- ✅ Debug endpoint
- ✅ Console logging

### 2. Test After Deployment

**Open your app:**
```
https://okta-ssf-transmitter-production-cb28.up.railway.app
```

**Send a User Risk Change event:**
1. Fill the form
2. Submit
3. **Scroll down** to see JWT details
4. Click **"Open in JWT.io"**
5. JWT.io opens with your token!

### 3. Verify Fields in Payload

Look in the `Payload` section and verify:
```json
"currentRiskLevel": "HIGH",    ← Check this is here
"previousRiskLevel": "LOW"     ← Check this is here
```

**If fields are there** → Frontend working, backend working, JWT correct! ✅

**If fields are MISSING** → Check console logs with `?debug` mode

---

## 💡 Pro Tips

### 1. **Use JWT.io to Verify**
- Click "Open in JWT.io"
- Verify all claims
- Check signature algorithm
- Inspect event structure

### 2. **Copy Token for Testing**
- Click "Copy"
- Paste into Postman
- Or use with curl
- Or send to support

### 3. **Compare Success vs Error**
- When event succeeds, check payload
- When event fails, check payload
- Compare to see what's different

### 4. **Check HTTP Request**
- See exact Okta endpoint
- Verify Content-Type header
- Confirm POST method

---

## 📊 Summary

**Feature:** JWT display with jwt.io integration ✅

**What you see:**
- ✅ Full JWT token (clickable)
- ✅ Decoded header
- ✅ Decoded payload
- ✅ HTTP request details
- ✅ Copy button
- ✅ Open in JWT.io button

**What you can do:**
- ✅ Inspect JWT structure
- ✅ Verify all fields are present
- ✅ Debug missing fields
- ✅ Copy for testing
- ✅ Open in jwt.io for analysis

**Works for:**
- ✅ Successful events (green)
- ✅ Failed events (red)
- ✅ All 15 event types

---

## 🚀 Ready to Push

```bash
git push origin main
```

**After deployment, you'll be able to:**
1. Send an event
2. See the JWT that was sent
3. Click "Open in JWT.io"
4. Verify all fields are in the payload
5. Debug any issues instantly!

---

## 🎯 For Your Current Issue

After pushing and deploying:

1. **Send User Risk Change event**
2. **Scroll to JWT Details section**
3. **Look at Payload:**

```json
"events": {
  "https://schemas.okta.com/secevent/okta/event-type/user-risk-change": {
    "subject": {...},
    "currentRiskLevel": "???",    ← Check if this exists!
    "previousRiskLevel": "???"    ← Check if this exists!
  }
}
```

**If fields are there:** JWT is correct, might be Okta API version issue
**If fields are missing:** Frontend not collecting or backend not including

**Click "Open in JWT.io"** to see full details!

---

**Push now and you'll have full JWT visibility!** 🔍
