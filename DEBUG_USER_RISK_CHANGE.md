# Debug Guide - User Risk Change Event

## 🐛 Issue

UI shows the risk level dropdowns, but Okta still says fields are blank:
```json
{
  "err": "invalid_request",
  "description": "previousRiskLevel: The field cannot be left blank, currentRiskLevel: The field cannot be left blank"
}
```

**This means the field values aren't making it into the JWT payload sent to Okta.**

---

## 🔍 Debugging Steps

### Step 1: Check Browser Console

1. **Open your Railway app:**
   ```
   https://okta-ssf-transmitter-production-cb28.up.railway.app
   ```

2. **Open browser DevTools:**
   - Chrome: F12 or Cmd+Option+I (Mac)
   - Go to "Console" tab

3. **Select "User Risk Change (Okta)"**

4. **Fill the dropdowns:**
   - Current: HIGH
   - Previous: LOW

5. **Click "Send Security Event"**

6. **Check Console Output:**

Look for these messages:
```javascript
Event type data: {label: "User Risk Change", ...}
Field definitions: [{name: "currentRiskLevel", ...}, ...]
Collecting field: currentRiskLevel, ID: currentRiskLevel, Element: <select...>
  Value: HIGH
  Added to formData: currentRiskLevel = HIGH
Collecting field: previousRiskLevel, ID: previousRiskLevel, Element: <select...>
  Value: LOW
  Added to formData: previousRiskLevel = LOW
Final formData to send: {subject: "...", eventType: "USER_RISK_CHANGE", currentRiskLevel: "HIGH", previousRiskLevel: "LOW"}
```

**What to look for:**
- ✅ If you see "Added to formData" → Frontend is working
- ❌ If you see "Element not found" → Frontend issue
- ❌ If no logs appear → JavaScript error (check for red errors in console)

### Step 2: Use Debug Mode

Add `?debug` to your URL:

```
https://okta-ssf-transmitter-production-cb28.up.railway.app?debug
```

Now when you submit:
1. It sends to `/api/debug-event` instead
2. Shows alert with debug info
3. Check console for full response
4. See exactly what JWT would be generated

### Step 3: Test with cURL

Bypass the UI completely:

```bash
curl -X POST https://okta-ssf-transmitter-production-cb28.up.railway.app/api/debug-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test@yourcompany.com",
    "eventType": "USER_RISK_CHANGE",
    "currentRiskLevel": "HIGH",
    "previousRiskLevel": "LOW",
    "reason": "Test"
  }'
```

**Expected response:**
```json
{
  "status": "debug",
  "received_data": { ... },
  "extra_fields_collected": {
    "currentRiskLevel": "HIGH",
    "previousRiskLevel": "LOW"
  },
  "jwt_payload": {
    "events": {
      "https://schemas.okta.com/secevent/okta/event-type/user-risk-change": {
        "subject": {...},
        "currentRiskLevel": "HIGH",
        "previousRiskLevel": "LOW",
        "reason": "Test"
      }
    }
  }
}
```

**If this works but UI doesn't, it's a frontend issue.**
**If this also fails, it's a backend issue.**

### Step 4: Check Railway Logs

1. Go to Railway dashboard
2. Click your service
3. Go to "Deployments" → Latest → "View Logs"
4. Look for lines starting with `[INFO]` or `[ERROR]`

**Look for:**
```
[INFO] Debug - Received data: {...}
[INFO] Debug - Field currentRiskLevel: HIGH
[INFO] Debug - Field previousRiskLevel: LOW
[INFO] Debug - Extra fields: {'currentRiskLevel': 'HIGH', 'previousRiskLevel': 'LOW'}
```

---

## 🔧 Possible Issues & Fixes

### Issue 1: Old Code Still Deployed

**Symptom:** Dropdowns show but values not collected

**Cause:** You're testing with old deployment that doesn't have new code

**Fix:**
```bash
# Check what's deployed
git log origin/main -1

# Should show recent commit about dynamic forms
# If not, push again:
git push origin main --force
```

### Issue 2: JavaScript Error

**Symptom:** No console logs appear

**Cause:** JavaScript error preventing code execution

**Fix:**
1. Open browser console
2. Look for RED error messages
3. Share the error message

### Issue 3: Field IDs Don't Match

**Symptom:** Console shows "Element not found!"

**Cause:** ID mismatch between HTML generation and collection

**Fix:** Check the generated HTML:
1. Right-click on dropdown → "Inspect Element"
2. Look at the `id` attribute
3. Should be `id="currentRiskLevel"`

### Issue 4: Event Types Not Loading

**Symptom:** Dropdowns never appear

**Cause:** API call failing

**Fix:**
```bash
# Check if API returns field_definitions
curl https://your-app.railway.app/api/event-types | jq '.USER_RISK_CHANGE.field_definitions'

# Should show array with currentRiskLevel and previousRiskLevel
```

---

## 🎯 Quick Verification

### Test 1: Check API Returns Schemas

```bash
curl https://okta-ssf-transmitter-production-cb28.up.railway.app/api/event-types \
  | jq '.USER_RISK_CHANGE'
```

**Expected:**
```json
{
  "uri": "https://schemas.okta.com/secevent/okta/event-type/user-risk-change",
  "label": "User Risk Change (Okta)",
  "description": "User risk level has changed...",
  "category": "Okta Specific",
  "extra_fields": [...],
  "field_definitions": [
    {
      "name": "currentRiskLevel",
      "required": true,
      "label": "Current Risk Level",
      "type": "select",
      "options": [...]
    },
    {
      "name": "previousRiskLevel",
      "required": true,
      "label": "Previous Risk Level",
      "type": "select",
      "options": [...]
    }
  ]
}
```

**If missing `field_definitions`, backend not updated yet.**

### Test 2: Test Debug Endpoint

```bash
curl -X POST https://okta-ssf-transmitter-production-cb28.up.railway.app/api/debug-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test@yourcompany.com",
    "eventType": "USER_RISK_CHANGE",
    "currentRiskLevel": "HIGH",
    "previousRiskLevel": "LOW"
  }'
```

**Check if `extra_fields_collected` shows the risk levels.**

---

## 📋 Step-by-Step Debugging Checklist

Run through these in order:

- [ ] **Push latest code**
  ```bash
  git push origin main
  ```

- [ ] **Wait for Railway deployment** (2 minutes)

- [ ] **Check API endpoint**
  ```bash
  curl YOUR_URL/api/event-types | jq '.USER_RISK_CHANGE.field_definitions'
  ```
  Should show field definitions

- [ ] **Open UI with debug mode**
  ```
  https://your-app.railway.app?debug
  ```

- [ ] **Open browser console** (F12)

- [ ] **Select User Risk Change event**
  - Check console: "Field definitions: [...]"

- [ ] **Check if dropdowns appeared**
  - Should see 2 dropdowns
  - Inspect element: `id="currentRiskLevel"`

- [ ] **Fill dropdowns**
  - Current: HIGH
  - Previous: LOW

- [ ] **Submit form (debug mode)**
  - Check console logs
  - Alert should appear with debug info

- [ ] **Check formData in console**
  ```javascript
  Final formData to send: {
    subject: "...",
    eventType: "USER_RISK_CHANGE",
    currentRiskLevel: "HIGH",    ← Should be here!
    previousRiskLevel: "LOW"      ← Should be here!
  }
  ```

- [ ] **If fields NOT in formData** → Frontend collection issue

- [ ] **If fields IN formData** → Backend processing issue

- [ ] **Test with regular mode** (remove ?debug)

- [ ] **Check Railway logs** for backend debugging output

---

## 🆘 If Still Not Working

Share these with me:

1. **Browser Console Output** (copy/paste all messages)
2. **Debug endpoint response** (from the cURL test)
3. **Railway logs** (last 50 lines)
4. **Screenshot** of the form with dropdowns

I can then identify the exact issue!

---

## 🚀 Quick Fix to Try Now

**Before pushing**, ensure your browser isn't caching old JavaScript:

1. **Hard refresh:**
   - Chrome/Firefox: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)
   - Safari: Cmd+Option+R

2. **Or clear cache:**
   - DevTools → Network tab → "Disable cache" checkbox
   - Refresh page

3. **Test again**

Sometimes the browser caches old JavaScript code!

---

## 📊 Expected vs Actual

### What Should Happen:

```
User selects "User Risk Change"
  ↓
2 dropdowns appear ✅ (you see this)
  ↓
User selects HIGH and LOW
  ↓
JavaScript collects: currentRiskLevel: "HIGH", previousRiskLevel: "LOW"
  ↓
Sent to backend in JSON
  ↓
Backend adds to JWT
  ↓
JWT sent to Okta with fields
  ↓
Success! ✅
```

### What's Happening:

```
User selects "User Risk Change"
  ↓
2 dropdowns appear ✅
  ↓
User selects HIGH and LOW
  ↓
JavaScript doesn't collect values ❌ (or collects but doesn't send)
  ↓
Sent to backend WITHOUT risk level fields
  ↓
Backend generates JWT without risk levels
  ↓
JWT sent to Okta missing fields
  ↓
Okta rejects ❌
```

---

## 🎯 Most Likely Issue

**You're testing with old deployment that doesn't have the new dynamic collection code.**

**Solution:**
```bash
# Push the latest changes
git push origin main

# Wait 2 minutes for Railway to deploy

# Hard refresh browser (Cmd+Shift+R)

# Test again
```

---

**Push the new code and use the debugging steps above to identify the exact issue!** 🔍
