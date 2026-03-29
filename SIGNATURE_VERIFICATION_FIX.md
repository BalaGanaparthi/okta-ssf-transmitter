# Fix: Signature Verification Error

## Error You're Seeing

```json
{
    "err": "authentication_failed",
    "description": "Could not verify message signature, Verification failed for kid=transmitter-key-1"
}
```

## Root Cause

The **private key** used to sign the JWT doesn't match the **public key** that Okta has registered. This happens when:

1. Keys were regenerated after Okta registration
2. Okta was registered with a different JWKS endpoint
3. The keys in `certs/` folder don't match what's deployed

## What I Fixed

### 1. Disabled Auto-Generation ✅

**Before:** Keys were auto-generated if missing (causing mismatches)

**After:** Keys MUST exist in `certs/` folder and will NEVER be auto-generated

The app will now **fail to start** with a clear error if keys are missing, preventing silent key mismatches.

### 2. Added Verification Endpoint ✅

New endpoint to verify which keys are being used:
```
GET /api/verify-keys
```

This shows:
- Key ID being used
- Public key fingerprint
- JWKS details

## Solution Steps

### Step 1: Commit and Deploy the Fix

```bash
# Stage changes
git add src/ssf_transmitter/core/key_manager.py
git add src/ssf_transmitter/api/routes.py

# Commit
git commit -m "Fix: Disable key auto-generation, add key verification endpoint"

# Push
git push origin main
```

Wait for Railway to redeploy (~2 minutes).

### Step 2: Verify Keys Are Correct

**Check which keys are deployed:**

```bash
# Replace with your Railway URL
curl https://your-app.railway.app/api/verify-keys
```

**Expected response:**
```json
{
  "status": "success",
  "key_id": "transmitter-key-1",
  "public_key_fingerprint": "a1b2c3d4e5f6...",
  "public_key_sha256_short": "a1b2c3d4e5f6...",
  "jwks_kid": "transmitter-key-1",
  "jwks_n_length": 342,
  "message": "Keys are loaded and valid",
  "note": "Compare this fingerprint with Okta registration to verify keys match"
}
```

**Save the fingerprint** - you'll need it to verify.

### Step 3: Get Current JWKS

```bash
# Get the JWKS that's currently being served
curl https://your-app.railway.app/.well-known/jwks.json > current_jwks.json

# View it
cat current_jwks.json
```

You should see something like:
```json
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "transmitter-key-1",
      "alg": "RS256",
      "n": "uyGQgrQKmMMyJksDDgJr...",
      "e": "AQAB"
    }
  ]
}
```

### Step 4: Re-Register Provider with Okta

**This is the critical step!** You need to update Okta with the current JWKS.

#### Option A: Delete and Re-Register (Recommended)

**1. Get your provider ID:**

```bash
OKTA_DOMAIN="https://your-org.okta.com"
OKTA_API_TOKEN="your-api-token"

# List providers
curl -X GET "$OKTA_DOMAIN/api/v1/security/api/v1/security-events-providers" \
  -H "Authorization: SSWS $OKTA_API_TOKEN"

# Look for your "SSF Transmitter" and note the "id" field
# Example: "id": "sep123abc456"
```

**2. Delete the old provider:**

```bash
PROVIDER_ID="sep123abc456"  # Replace with your actual ID

curl -X DELETE "$OKTA_DOMAIN/api/v1/security/api/v1/security-events-providers/$PROVIDER_ID" \
  -H "Authorization: SSWS $OKTA_API_TOKEN"
```

**3. Register with current JWKS:**

```bash
RAILWAY_URL="https://your-app.railway.app"

curl -X POST "$OKTA_DOMAIN/api/v1/security/api/v1/security-events-providers" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SSF Transmitter",
    "issuer": "'$RAILWAY_URL'",
    "jwks_url": "'$RAILWAY_URL'/.well-known/jwks.json"
  }'
```

**Expected response:**
```json
{
  "id": "sep789xyz123",
  "name": "SSF Transmitter",
  "issuer": "https://your-app.railway.app",
  "jwks_url": "https://your-app.railway.app/.well-known/jwks.json",
  "status": "ACTIVE",
  ...
}
```

#### Option B: Update Existing Provider

If deletion is not possible, update the existing provider:

```bash
PROVIDER_ID="sep123abc456"  # Your actual provider ID
RAILWAY_URL="https://your-app.railway.app"

curl -X PUT "$OKTA_DOMAIN/api/v1/security/api/v1/security-events-providers/$PROVIDER_ID" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SSF Transmitter",
    "issuer": "'$RAILWAY_URL'",
    "jwks_url": "'$RAILWAY_URL'/.well-known/jwks.json"
  }'
```

### Step 5: Test Again

**Wait 1-2 minutes for Okta to refresh the JWKS**, then test:

**Via Postman or cURL:**

```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test.user@yourcompany.com",
    "eventType": "CREDENTIAL_CHANGE_REQUIRED",
    "reason": "Testing after re-registration"
  }'
```

**Expected response:**
```json
{
  "success": true,
  "status": 202,
  "data": {
    "message": "Event accepted"
  }
}
```

**No more signature verification errors!** ✅

### Step 6: Verify in Okta Logs

1. Go to Okta Admin Console
2. **Reports** → **System Log**
3. Search for your test user
4. You should see the event logged

## Understanding the Fix

### Before (Problem):

```
┌─────────────────────────────────────────────────────────────┐
│ Railway Deployment 1                                        │
│ ├── Keys auto-generated: Key A                             │
│ └── JWKS served: Public Key A                              │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Okta Registration                                           │
│ └── Registered with: Public Key A ✓                        │
└─────────────────────────────────────────────────────────────┘

    [Time passes, Railway restarts or redeploys]

┌─────────────────────────────────────────────────────────────┐
│ Railway Deployment 2                                        │
│ ├── Keys auto-generated AGAIN: Key B  ⚠️                   │
│ └── JWKS served: Public Key B                              │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Event Sent                                                  │
│ └── Signed with: Private Key B                             │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Okta Verification                                           │
│ ├── Has: Public Key A                                      │
│ ├── Receives JWT signed with: Private Key B                │
│ └── Result: SIGNATURE VERIFICATION FAILED ❌                │
└─────────────────────────────────────────────────────────────┘
```

### After (Fixed):

```
┌─────────────────────────────────────────────────────────────┐
│ Git Repository                                              │
│ └── certs/                                                  │
│     ├── private_key.pem (committed)                         │
│     └── public_key.pem (committed)                          │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Railway Deployment (Any Time)                               │
│ ├── Keys loaded from git: Key A                            │
│ ├── NO auto-generation                                     │
│ └── JWKS always serves: Public Key A ✓                     │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Okta Registration                                           │
│ └── Registered with: Public Key A ✓                        │
└─────────────────────────────────────────────────────────────┘

    [Time passes, Railway restarts or redeploys]

┌─────────────────────────────────────────────────────────────┐
│ Railway Deployment (Still uses same keys)                   │
│ ├── Keys loaded from git: Key A                            │
│ └── JWKS served: Public Key A ✓                            │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Event Sent                                                  │
│ └── Signed with: Private Key A ✓                           │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Okta Verification                                           │
│ ├── Has: Public Key A                                      │
│ ├── Receives JWT signed with: Private Key A                │
│ └── Result: SUCCESS ✅                                      │
└─────────────────────────────────────────────────────────────┘
```

## Key Points

### ✅ What's Fixed

1. **No More Auto-Generation:** Keys will NEVER be auto-generated
2. **Git-Tracked Keys:** Keys in `certs/` are committed and deployed
3. **Consistent Keys:** Same keys used across all deployments
4. **Verification Endpoint:** Can check which keys are active

### ⚠️ Important

- The keys in `certs/` folder ARE committed to git
- They ARE deployed to Railway
- They will NOT regenerate
- But you MUST re-register with Okta to use the current keys

### 🔐 Security Note

For production, consider:
- Using Railway's persistent volumes for keys
- Or storing keys in environment variables (base64 encoded)
- Or using a secrets management service (AWS KMS, Vault, etc.)

But for now, git-tracked keys work fine for testing/development.

## Quick Verification Checklist

After following the steps:

- [ ] Code changes committed and pushed
- [ ] Railway redeployed successfully
- [ ] `/api/verify-keys` endpoint returns success
- [ ] `/.well-known/jwks.json` is accessible
- [ ] Provider re-registered in Okta
- [ ] Test event sent successfully (no signature error)
- [ ] Event appears in Okta System Log

## If It Still Fails

### Check 1: Verify Keys Are Deployed

```bash
# SSH into Railway (if possible) or check logs
# Look for this in startup logs:
# "✓ Keys found in certs/ folder"
# "✓ Keys validated successfully"
```

### Check 2: Compare JWKS

**Get local JWKS:**
```bash
cd project005-SSF
python3 -c "
from src.ssf_transmitter.core.key_manager import KeyManager
from pathlib import Path
km = KeyManager('certs/private_key.pem', 'certs/public_key.pem')
import json
print(json.dumps(km.get_jwks('transmitter-key-1'), indent=2))
"
```

**Get deployed JWKS:**
```bash
curl https://your-app.railway.app/.well-known/jwks.json
```

**Compare them - they should be IDENTICAL!**

### Check 3: Verify Okta Has Current JWKS

Okta caches the JWKS. You might need to:
1. Wait 5-10 minutes for cache to expire
2. Or delete and re-register the provider
3. Or contact Okta support to clear cache

### Check 4: Check Railway Logs

In Railway dashboard:
- Go to Deployments → Latest
- View logs
- Look for key loading messages
- Check for any errors

## Summary

**What you need to do:**

1. ✅ Commit and push the code changes (I made)
2. ✅ Wait for Railway to redeploy
3. ✅ Re-register the provider in Okta with current JWKS
4. ✅ Test sending an event
5. ✅ Verify in Okta logs

**The signature verification error should be gone!** 🎉
