# Complete Setup, Deployment & Testing Guide

**SSF Transmitter - From Zero to Production**

Follow these steps exactly to set up, deploy, configure, and test your SSF Transmitter.

---

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Phase 1: Local Setup](#phase-1-local-setup)
3. [Phase 2: Railway Deployment](#phase-2-railway-deployment)
4. [Phase 3: Okta Configuration](#phase-3-okta-configuration)
5. [Phase 4: Testing & Verification](#phase-4-testing--verification)
6. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before you begin, ensure you have:

- [ ] **Python 3.9+** installed
  ```bash
  python3 --version
  # Should show 3.9 or higher
  ```

- [ ] **Git** installed
  ```bash
  git --version
  ```

- [ ] **GitHub account** (for deployment)

- [ ] **Railway account** (free tier)
  - Sign up at: https://railway.app/

- [ ] **Okta organization** with Identity Threat Protection enabled
  - You need admin access
  - Must have ITP (Identity Threat Protection) feature

- [ ] **Test user in Okta** (for sending test events)

---

## Phase 1: Local Setup

### Step 1.1: Prepare the Project

```bash
# Navigate to project directory
cd project005-SSF

# Verify you're in the right place
ls -la
# You should see: src/, tests/, docs/, wsgi.py, etc.
```

### Step 1.2: Create Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Your prompt should now show (venv)
```

### Step 1.3: Install Dependencies

```bash
# Upgrade pip
pip install --upgrade pip

# Install all dependencies
pip install -r requirements.txt

# This installs:
# - Flask (web framework)
# - flask-cors (CORS support)
# - PyJWT (JWT handling)
# - cryptography (RSA keys)
# - requests (HTTP client)
# - gunicorn (production server)
# - pytest (testing)
```

### Step 1.4: Configure Environment Variables

```bash
# Copy environment template
cp .env.example .env

# Edit .env file
nano .env
# or use your favorite editor: code .env, vim .env, etc.
```

**Set these values in `.env`:**

```env
# For local testing, use localhost
ISSUER=http://localhost:8080

# Your Okta organization domain
OKTA_DOMAIN=https://your-org.okta.com

# Key ID for JWKS (can leave as default)
KEY_ID=transmitter-key-1

# Port (can leave as default)
PORT=8080
```

**Replace `your-org` with your actual Okta domain!**

Save and close the file.

### Step 1.5: Run the Application

```bash
# Set PYTHONPATH
export PYTHONPATH=$PWD

# Run the application
python wsgi.py
```

**You should see:**
```
╔══════════════════════════════════════════════════════════════╗
║          SSF Transmitter Web Application                     ║
╚══════════════════════════════════════════════════════════════╝

🌐 Server starting on 0.0.0.0:8080
🔑 JWKS endpoint: /.well-known/jwks.json
📡 Issuer: http://localhost:8080
🎯 Okta Domain: https://your-org.okta.com

Press Ctrl+C to stop
```

**Keys will be auto-generated on first run:**
```
[INFO] Generating new RSA key pair...
[INFO] Keys generated successfully
```

### Step 1.6: Test Locally

**Open a NEW terminal (keep the server running):**

#### Test 1: Health Check
```bash
curl http://localhost:8080/health
# Expected: {"status":"healthy"}
```

#### Test 2: JWKS Endpoint
```bash
curl http://localhost:8080/.well-known/jwks.json
# Expected: JSON with RSA public key
```

#### Test 3: Web UI
```bash
# Open in browser
open http://localhost:8080
# or visit http://localhost:8080 manually
```

**You should see:**
- Beautiful animated starfield background
- "SSF Transmitter" header
- Form with user email, event type dropdown, and reason fields
- Configuration panel showing your settings

#### Test 4: Configuration API
```bash
curl http://localhost:8080/api/config
# Expected: JSON with issuer, oktaDomain, keyId, jwksUrl
```

#### Test 5: Event Types API
```bash
curl http://localhost:8080/api/event-types
# Expected: JSON with three event types
```

### Step 1.7: Run Automated Tests

```bash
# In the NEW terminal (not the server terminal)
cd project005-SSF
source venv/bin/activate
export PYTHONPATH=$PWD

# Run all tests
pytest -v

# Expected output:
# ======================== 13 passed in 0.58s =========================
```

**All 13 tests should pass!** ✅

### Step 1.8: Stop Local Server

```bash
# In the server terminal, press:
Ctrl+C

# Server should stop gracefully
```

**✅ Phase 1 Complete!** Your application works locally.

---

## Phase 2: Railway Deployment

### Step 2.1: Prepare Git Repository

```bash
# Initialize git if not already done
git init

# Add all files
git add .

# Commit
git commit -m "SSF Transmitter - Production ready"
```

### Step 2.2: Create GitHub Repository

**Option A: Via GitHub Website**

1. Go to https://github.com
2. Click the "+" icon → "New repository"
3. Name: `ssf-transmitter` (or your preferred name)
4. Description: "SSF Transmitter for Okta"
5. Public or Private (your choice)
6. **DO NOT** initialize with README
7. Click "Create repository"

**Option B: Via GitHub CLI**

```bash
# If you have gh CLI installed
gh repo create ssf-transmitter --public --source=. --remote=origin
```

### Step 2.3: Push to GitHub

```bash
# Add remote (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/ssf-transmitter.git

# Push code
git branch -M main
git push -u origin main
```

**Verify:** Visit your GitHub repository URL - you should see all your files.

### Step 2.4: Deploy to Railway

#### A. Sign Up / Log In to Railway

1. Go to https://railway.app/
2. Click "Login"
3. Sign in with GitHub
4. Authorize Railway to access your repositories

#### B. Create New Project

1. Click "**New Project**"
2. Select "**Deploy from GitHub repo**"
3. Choose your `ssf-transmitter` repository
4. Click "**Deploy**"

#### C. Wait for Initial Build

Railway will:
- Detect your Dockerfile ✅
- Build the Docker image
- Deploy the container

**This takes 2-3 minutes.**

Watch the logs in Railway dashboard - you'll see:
```
Building...
Pushing...
Deploying...
```

**Initial deployment will FAIL** - this is expected! We need to set environment variables first.

### Step 2.5: Configure Environment Variables

#### A. Open Settings

1. In Railway dashboard, click your service
2. Click "**Variables**" tab

#### B. Add Environment Variables

Click "**+ New Variable**" for each:

```
Variable 1:
Name: ISSUER
Value: https://your-app.railway.app
(We'll update this in the next step)

Variable 2:
Name: OKTA_DOMAIN
Value: https://your-org.okta.com
(Replace your-org with your actual Okta domain)

Variable 3:
Name: KEY_ID
Value: transmitter-key-1

Variable 4:
Name: FLASK_ENV
Value: production
```

**IMPORTANT:** Replace `your-org` with your actual Okta organization subdomain!

Click "**Save**" or changes are auto-saved.

### Step 2.6: Generate Railway Domain

#### A. Get Your Public URL

1. Go to "**Settings**" tab
2. Scroll to "**Networking**" section
3. Under "**Public Networking**", click "**Generate Domain**"
4. Railway will create a URL like: `your-app.railway.app`

**Copy this URL!** You'll need it in the next step.

#### B. Update ISSUER Variable

1. Go back to "**Variables**" tab
2. Find the `ISSUER` variable
3. Update it to your actual Railway URL:
   ```
   https://your-actual-app-name.railway.app
   ```
4. Save

### Step 2.7: Redeploy

Railway will automatically redeploy when you change variables.

**Or manually trigger:**
1. Go to "**Deployments**" tab
2. Click "**Redeploy**" on the latest deployment

**Wait for deployment to complete** (~2 minutes)

### Step 2.8: Verify Deployment

#### A. Check Deployment Status

In Railway dashboard:
- Status should show "**Active**" (green dot)
- No errors in logs

#### B. Test Health Check

```bash
# Replace with your actual Railway URL
curl https://your-app.railway.app/health

# Expected: {"status":"healthy"}
```

#### C. Test JWKS Endpoint

```bash
# Replace with your actual Railway URL
curl https://your-app.railway.app/.well-known/jwks.json

# Expected: JSON with public key
```

#### D. Visit Web UI

```bash
# Open in browser
open https://your-app.railway.app

# or visit manually
```

**You should see the beautiful SSF Transmitter UI!**

**✅ Phase 2 Complete!** Your application is deployed to Railway.

---

## Phase 3: Okta Configuration

### Step 3.1: Generate Okta API Token

1. **Log in to Okta Admin Console**
   - Go to your Okta org: `https://your-org.okta.com`
   - Log in as an administrator

2. **Navigate to API Tokens**
   - Click **Security** → **API**
   - Click **Tokens** tab

3. **Create Token**
   - Click "**Create Token**"
   - Name: `SSF Transmitter Integration`
   - Click "**Create Token**"
   - **IMPORTANT:** Copy the token immediately!
   - Save it somewhere safe (you won't see it again)

**Your token looks like:** `00abc123def456ghi789...`

### Step 3.2: Verify JWKS Accessibility

Before registering with Okta, ensure your JWKS endpoint is publicly accessible:

```bash
# Test from your local machine
curl https://your-app.railway.app/.well-known/jwks.json

# Should return:
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "transmitter-key-1",
      "alg": "RS256",
      "n": "...",
      "e": "AQAB"
    }
  ]
}
```

**If this fails, your JWKS won't work with Okta!**

### Step 3.3: Register SSF Provider in Okta

You'll make an API call to Okta to register your transmitter as an SSF provider.

**Prepare your command:**

```bash
# Set variables (replace with your values)
OKTA_DOMAIN="https://your-org.okta.com"
OKTA_API_TOKEN="00abc123def456ghi789..."
RAILWAY_URL="https://your-app.railway.app"

# Register provider
curl -X POST "$OKTA_DOMAIN/api/v1/security/api/v1/security-events-providers" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{
    "name": "SSF Transmitter",
    "issuer": "'$RAILWAY_URL'",
    "jwks_url": "'$RAILWAY_URL'/.well-known/jwks.json"
  }'
```

**Expected Response (200 OK):**
```json
{
  "id": "sep123abc456",
  "name": "SSF Transmitter",
  "issuer": "https://your-app.railway.app",
  "jwks_url": "https://your-app.railway.app/.well-known/jwks.json",
  "status": "ACTIVE",
  "created": "2024-03-29T10:00:00.000Z",
  "_links": { ... }
}
```

**Save the `id` from the response!** You might need it later.

### Step 3.4: Verify Provider Registration

#### Option A: Via API

```bash
# List all providers
curl -X GET "$OKTA_DOMAIN/api/v1/security/api/v1/security-events-providers" \
  -H "Authorization: SSWS $OKTA_API_TOKEN"

# Look for your "SSF Transmitter" in the list
```

#### Option B: Via Okta Admin Console (if available)

1. Go to **Security** → **Identity Threat Protection**
2. Look for **Signal Providers** or **Security Events Providers**
3. You should see "SSF Transmitter" listed

**Note:** Not all Okta orgs have this UI available.

**✅ Phase 3 Complete!** Okta is configured to receive events from your transmitter.

---

## Phase 4: Testing & Verification

### Step 4.1: Send Test Event via Web UI

1. **Open your Railway URL** in browser:
   ```
   https://your-app.railway.app
   ```

2. **Fill in the form:**
   - **User Email:** Enter an email of an existing Okta user
     - Example: `john.doe@yourcompany.com`
     - **IMPORTANT:** This user MUST exist in your Okta org!

   - **Event Type:** Select "**Credential Change Required**" from dropdown

   - **Reason (Optional):** Enter a reason
     - Example: `Testing SSF integration`

3. **Click "Send Security Event"**

4. **Check for success:**
   - You should see a green success message
   - Status indicator shows the event was sent
   - Response panel shows: "✅ Success"

### Step 4.2: Verify in Okta Logs

1. **Go to Okta Admin Console**
   - Navigate to **Reports** → **System Log**

2. **Filter logs:**
   - Time: Last 15 minutes
   - Search for: `security.threat.detected` or your user's email

3. **Look for event:**
   You should see an entry like:
   ```
   Event: security.threat.detected
   Actor: System
   Target: john.doe@yourcompany.com
   Outcome: Success
   ```

4. **Click on the event** to see details:
   - Event Type
   - Reason
   - Source (your Railway URL)

**If you see this, it worked!** 🎉

### Step 4.3: Test All Event Types

#### Test 1: Credential Change Required

**Via UI:**
1. User: `test.user@yourcompany.com` (existing user)
2. Event Type: "Credential Change Required"
3. Reason: "Password found in data breach"
4. Send

**Via cURL:**
```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test.user@yourcompany.com",
    "eventType": "CREDENTIAL_CHANGE_REQUIRED",
    "reason": "Password found in data breach"
  }'
```

#### Test 2: Account Disabled

**Via UI:**
1. User: `test.user@yourcompany.com`
2. Event Type: "Account Disabled"
3. Reason: "Multiple failed login attempts"
4. Send

**Via cURL:**
```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test.user@yourcompany.com",
    "eventType": "ACCOUNT_DISABLED",
    "reason": "Multiple failed login attempts"
  }'
```

#### Test 3: Account Enabled

**Via UI:**
1. User: `test.user@yourcompany.com`
2. Event Type: "Account Enabled"
3. Reason: "Investigation completed - user verified"
4. Send

**Via cURL:**
```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test.user@yourcompany.com",
    "eventType": "ACCOUNT_ENABLED",
    "reason": "Investigation completed - user verified"
  }'
```

### Step 4.4: Check All Events in Okta

1. Return to **Reports** → **System Log**
2. Filter by the test user email
3. You should see **all 3 events** in chronological order

### Step 4.5: Test Error Handling

#### Test Invalid User

```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "nonexistent@example.com",
    "eventType": "CREDENTIAL_CHANGE_REQUIRED",
    "reason": "Testing error handling"
  }'

# Expected: Error response indicating user not found
```

#### Test Invalid Email Format

**Via UI:**
1. User: `not-an-email`
2. Event Type: Any
3. Send

**Expected:** Client-side validation error (email format invalid)

#### Test Missing Required Fields

```bash
curl -X POST https://your-app.railway.app/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "eventType": "CREDENTIAL_CHANGE_REQUIRED"
  }'

# Expected: {"error":"Subject and event type are required"}
```

**✅ Phase 4 Complete!** All testing verified.

---

## Troubleshooting

### Issue 1: Local Server Won't Start

**Symptom:** `python wsgi.py` fails

**Solutions:**

1. **Check Python version:**
   ```bash
   python3 --version
   # Must be 3.9+
   ```

2. **Verify virtual environment:**
   ```bash
   which python
   # Should show: /path/to/project005-SSF/venv/bin/python
   ```

3. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Check PYTHONPATH:**
   ```bash
   export PYTHONPATH=$PWD
   echo $PYTHONPATH
   ```

5. **Check port availability:**
   ```bash
   lsof -i :8080
   # If something is using port 8080, change PORT in .env
   ```

### Issue 2: Railway Build Fails

**Symptom:** Build fails in Railway dashboard

**Solutions:**

1. **Check Dockerfile exists:**
   ```bash
   ls -la Dockerfile
   ```

2. **Verify all files committed:**
   ```bash
   git status
   # Should show: "nothing to commit, working tree clean"
   ```

3. **Check Railway logs:**
   - Go to Deployments → Click failed deployment → View logs
   - Look for specific error messages

4. **Common fixes:**
   ```bash
   # Ensure these files exist
   ls requirements.txt
   ls wsgi.py
   ls src/ssf_transmitter/app.py
   ```

### Issue 3: JWKS Endpoint Returns 404

**Symptom:** `curl https://your-app.railway.app/.well-known/jwks.json` fails

**Solutions:**

1. **Check deployment status:**
   - Railway dashboard should show "Active"

2. **Check logs:**
   - Look for "Keys generated successfully" in logs

3. **Verify endpoint in local:**
   ```bash
   # Test locally first
   curl http://localhost:8080/.well-known/jwks.json
   ```

4. **Check certs directory:**
   - Keys should be auto-generated on startup

### Issue 4: Okta Provider Registration Fails

**Symptom:** API call returns error

**Common Errors:**

#### A. 401 Unauthorized
```json
{"errorCode":"E0000011","errorSummary":"Invalid token provided"}
```

**Fix:** Check your API token
- Generate a new token in Okta
- Ensure you copied the full token
- No extra spaces or characters

#### B. 400 Bad Request - Invalid JWKS URL
```json
{"errorCode":"E0000001","errorSummary":"JWKS URL is not accessible"}
```

**Fix:**
1. Verify JWKS is publicly accessible:
   ```bash
   curl https://your-app.railway.app/.well-known/jwks.json
   ```
2. Ensure Railway deployment is active
3. Check firewall/network settings

#### C. 403 Forbidden
```json
{"errorCode":"E0000006","errorSummary":"You do not have permission"}
```

**Fix:**
- Use admin account with proper permissions
- Ensure Identity Threat Protection feature is enabled
- Contact Okta support to enable SSF feature

### Issue 5: Events Not Appearing in Okta Logs

**Symptom:** Event sent successfully but not in Okta logs

**Solutions:**

1. **Check user exists:**
   - Verify the email is an actual user in Okta
   - Check spelling of email address

2. **Check Okta System Log filters:**
   - Remove all filters
   - Search for last 1 hour
   - Look for event type: `security.threat.detected`

3. **Check event response:**
   - 202 Accepted: Event queued (may take a few minutes)
   - 200 OK: Event processed immediately
   - 4xx: Error (check error message)

4. **Wait a few minutes:**
   - Events may take 1-5 minutes to appear in logs

5. **Verify provider is active:**
   ```bash
   curl -X GET "$OKTA_DOMAIN/api/v1/security/api/v1/security-events-providers" \
     -H "Authorization: SSWS $OKTA_API_TOKEN"
   ```
   - Check status: should be "ACTIVE"

### Issue 6: UI Not Loading

**Symptom:** Blank page or 404

**Solutions:**

1. **Check Railway URL:**
   - Use HTTPS, not HTTP
   - No trailing slash

2. **Check deployment logs:**
   - Look for errors on startup

3. **Test health endpoint:**
   ```bash
   curl https://your-app.railway.app/health
   ```

4. **Clear browser cache:**
   - Hard refresh: Cmd+Shift+R (Mac) or Ctrl+Shift+R (Windows)

### Issue 7: Tests Failing

**Symptom:** `pytest` shows failures

**Solutions:**

1. **Check PYTHONPATH:**
   ```bash
   export PYTHONPATH=$PWD
   ```

2. **Reinstall dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run specific test:**
   ```bash
   pytest tests/test_api.py::test_health_endpoint -v
   ```

4. **Check test output:**
   - Read the error message
   - Fix the specific issue

---

## Quick Reference

### Important URLs

```bash
# Local
http://localhost:8080                          # Web UI
http://localhost:8080/.well-known/jwks.json   # JWKS
http://localhost:8080/health                   # Health check

# Railway (replace with your URL)
https://your-app.railway.app                          # Web UI
https://your-app.railway.app/.well-known/jwks.json   # JWKS
https://your-app.railway.app/health                   # Health check

# Okta
https://your-org.okta.com                            # Admin Console
https://your-org.okta.com/admin/reports/system-log   # System Log
```

### Key Commands

```bash
# Local development
./scripts/dev.sh                    # Start dev server
python wsgi.py                      # Alternative start

# Testing
pytest -v                           # Run all tests
pytest tests/test_api.py -v        # Run specific tests
make test                           # Using Makefile

# Docker
docker build -t ssf-transmitter .   # Build image
docker run -p 8080:8080 ssf-transmitter  # Run container

# Git
git add .                           # Stage changes
git commit -m "message"             # Commit
git push                            # Push to GitHub
```

### Environment Variables

```env
# Required
ISSUER=https://your-app.railway.app
OKTA_DOMAIN=https://your-org.okta.com
KEY_ID=transmitter-key-1

# Optional
PORT=8080
FLASK_ENV=production
```

---

## Success Checklist

Use this to verify everything is working:

### Local Setup ✅
- [ ] Virtual environment created and activated
- [ ] Dependencies installed
- [ ] `.env` file configured
- [ ] Application starts without errors
- [ ] Health check returns 200
- [ ] JWKS endpoint returns valid JSON
- [ ] Web UI loads in browser
- [ ] All 13 tests pass

### Railway Deployment ✅
- [ ] Code pushed to GitHub
- [ ] Railway project created
- [ ] Deployment successful (no errors)
- [ ] Environment variables set
- [ ] Public domain generated
- [ ] Health check accessible
- [ ] JWKS endpoint publicly accessible
- [ ] Web UI loads from Railway URL

### Okta Configuration ✅
- [ ] API token generated
- [ ] JWKS endpoint accessible from internet
- [ ] Provider registered successfully
- [ ] Provider shows as ACTIVE
- [ ] Provider appears in Okta (if UI available)

### Testing ✅
- [ ] Test event sent via UI
- [ ] Success message displayed
- [ ] Event appears in Okta System Log
- [ ] All 3 event types tested
- [ ] Events show correct data
- [ ] Error handling tested
- [ ] Invalid user handled correctly

---

## Next Steps

Once everything is working:

1. **Production Use:**
   - Integrate with your security systems
   - Send real security events
   - Monitor Okta logs

2. **Monitoring:**
   - Set up alerts in Railway
   - Monitor Okta event logs
   - Track error rates

3. **Scaling:**
   - Adjust Railway resources if needed
   - Consider adding persistent volumes for keys
   - Implement key rotation

4. **Security:**
   - Add API authentication (future)
   - Implement rate limiting (future)
   - Regular key rotation

5. **Documentation:**
   - Document your specific use cases
   - Train team members
   - Create runbooks

---

## Support Resources

- **Project Documentation:** `docs/` folder
- **Architecture Guide:** `docs/ARCHITECTURE.md`
- **Okta Developer Docs:** https://developer.okta.com/
- **Railway Docs:** https://docs.railway.app/
- **OpenID Shared Signals:** https://openid.net/wg/sharedsignals/

---

## Summary

You've now successfully:

✅ Set up the application locally
✅ Deployed to Railway
✅ Configured Okta SSF receiver
✅ Tested all functionality
✅ Verified end-to-end flow

**Your SSF Transmitter is production-ready!** 🚀

You can now send security event tokens from your systems to Okta, enabling real-time security signal sharing and automated threat response.

---

**Last Updated:** March 29, 2026
**Version:** 1.0.0
