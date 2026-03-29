# Quick Fix Steps - Signature Verification Error

## What I Fixed

✅ **Disabled automatic key generation** - Keys will NEVER regenerate
✅ **Added verification endpoint** - Check which keys are active
✅ **Created helper script** - Easy re-registration with Okta
✅ **Comprehensive guide** - Full troubleshooting in SIGNATURE_VERIFICATION_FIX.md

## Do This Now (5 minutes)

### 1. Push the Changes

```bash
git push origin main
```

Wait for Railway to redeploy (~2 minutes).

### 2. Verify Keys Are Working

```bash
# Check verification endpoint (replace with your Railway URL)
curl https://your-app.railway.app/api/verify-keys
```

Expected: `"status": "success"`

### 3. Re-Register with Okta

**Option A: Use the Helper Script (Easiest)**

```bash
# Set your variables
export OKTA_DOMAIN="https://your-org.okta.com"
export OKTA_API_TOKEN="your-okta-api-token"
export RAILWAY_URL="https://your-app.railway.app"

# Run the script
./scripts/reregister-okta.sh
```

The script will:
- ✅ Verify JWKS is accessible
- ✅ Find existing provider
- ✅ Delete old provider (optional)
- ✅ Register new provider with current keys

**Option B: Manual Re-Registration**

```bash
# Delete old provider
curl -X DELETE "https://your-org.okta.com/api/v1/security/api/v1/security-events-providers/YOUR_PROVIDER_ID" \
  -H "Authorization: SSWS YOUR_API_TOKEN"

# Register new provider
curl -X POST "https://your-org.okta.com/api/v1/security/api/v1/security-events-providers" \
  -H "Authorization: SSWS YOUR_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SSF Transmitter",
    "issuer": "https://your-app.railway.app",
    "jwks_url": "https://your-app.railway.app/.well-known/jwks.json"
  }'
```

### 4. Test It

Wait 1-2 minutes, then test:

```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test.user@yourcompany.com",
    "eventType": "CREDENTIAL_CHANGE_REQUIRED",
    "reason": "Testing after fix"
  }'
```

**Expected: NO signature verification error!** ✅

```json
{
  "success": true,
  "status": 202
}
```

### 5. Verify in Okta

1. Go to Okta Admin Console
2. **Reports** → **System Log**
3. Search for your test user
4. Event should appear!

## Why This Happened

**Before:**
- Keys were auto-generated on each deployment
- Okta had old public key
- Your app used new private key
- Signature verification failed ❌

**After:**
- Keys are in `certs/` folder (committed to git)
- Same keys used on every deployment
- Okta gets updated public key
- Signature verification works ✅

## Files Created

1. **SIGNATURE_VERIFICATION_FIX.md** - Complete troubleshooting guide
2. **scripts/reregister-okta.sh** - Automated re-registration script
3. **QUICK_FIX_STEPS.md** - This file (quick reference)

## New Endpoint

```
GET /api/verify-keys
```

Returns:
- Key ID being used
- Public key fingerprint
- JWKS details
- Verification status

Use this anytime to check which keys are active!

## Summary

**Your task:**
1. ✅ Push changes: `git push origin main`
2. ✅ Wait for Railway to redeploy
3. ✅ Re-register with Okta (use helper script)
4. ✅ Test sending event
5. ✅ Verify in Okta logs

**Time needed:** ~5 minutes

**Result:** No more signature verification errors! 🎉

---

**Need more details?** See `SIGNATURE_VERIFICATION_FIX.md`
