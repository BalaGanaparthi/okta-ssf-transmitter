# Railway Deployment Fix

## Issue
Getting error: `python: can't open file '/app/app.py': [Errno 2] No such file or directory`

## Root Cause
The `railway.toml` file had the old start command (`python app.py`), but we reorganized the project structure. The new entry point is `wsgi.py` with the production server script.

## Fix Applied
Updated `railway.toml` to use the correct start command: `sh scripts/start.sh`

## Steps to Deploy the Fix

### 1. Commit the Change
```bash
cd project005-SSF

# Add the updated file
git add railway.toml

# Commit
git commit -m "Fix Railway deployment - update start command"

# Push to GitHub
git push origin main
```

### 2. Railway Will Auto-Deploy
Railway automatically detects the push and will redeploy with the new configuration.

### 3. Monitor the Deployment
1. Go to your Railway dashboard
2. Click on your service
3. Go to "Deployments" tab
4. Watch the new deployment

**You should see:**
```
Building...
✓ Build successful
Deploying...
✓ Deployment successful
```

### 4. Verify It's Working

Once deployed, test:

```bash
# Health check (replace with your Railway URL)
curl https://your-app.railway.app/health

# Expected: {"status":"healthy"}
```

```bash
# JWKS endpoint
curl https://your-app.railway.app/.well-known/jwks.json

# Expected: JSON with public key
```

```bash
# Open in browser
open https://your-app.railway.app
```

## If It Still Fails

If you still get errors, try this alternative approach:

### Option A: Remove startCommand (Let Dockerfile Handle It)

Edit `railway.toml` and remove the `startCommand` line entirely:

```toml
[build]
builder = "DOCKERFILE"
dockerfilePath = "Dockerfile"

[deploy]
# startCommand removed - will use Dockerfile CMD
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
restartPolicyMaxRetries = 10
```

Then commit and push again.

### Option B: Delete railway.toml Entirely

```bash
# Remove the file
git rm railway.toml

# Commit
git commit -m "Remove railway.toml - use Dockerfile CMD"

# Push
git push origin main
```

Railway will use the Dockerfile's `CMD` directly: `CMD ["sh", "scripts/start.sh"]`

### Option C: Check Railway Settings

If neither works, check Railway dashboard:

1. Click your service
2. Go to "Settings" tab
3. Scroll to "Deploy"
4. Look for "Start Command" override
5. If it's set to `python app.py`, **clear it**
6. Save and redeploy

## Verification Steps

After successful deployment:

### 1. Check Logs
In Railway dashboard → Deployments → Latest → View logs

**You should see:**
```
🚀 Starting SSF Transmitter (Production Mode)
[INFO] Keys already exist
[INFO] SSF Transmitter Application Started
[INFO] Environment: production
[INFO] Issuer: https://your-app.railway.app
[INFO] Okta Domain: https://your-org.okta.com
```

### 2. Test Endpoints

```bash
# Health
curl https://your-app.railway.app/health

# JWKS
curl https://your-app.railway.app/.well-known/jwks.json

# Config
curl https://your-app.railway.app/api/config
```

All should return 200 OK with proper JSON responses.

### 3. Test Web UI

Open in browser - you should see the beautiful SSF Transmitter interface with animated background.

## What Changed in Project Structure

For your reference:

**Old Structure:**
```
app.py              ← Entry point (root level)
templates/
static/
```

**New Structure:**
```
wsgi.py                           ← New entry point (root level)
scripts/start.sh                  ← Production start script
src/ssf_transmitter/
  ├── app.py                      ← Flask app factory (in package)
  ├── templates/
  └── static/
```

**Entry Points:**
- **Development:** `python wsgi.py`
- **Production:** `sh scripts/start.sh` (runs Gunicorn)
- **Docker CMD:** `CMD ["sh", "scripts/start.sh"]`

## Summary

**What we fixed:**
- ✅ Updated `railway.toml` start command from `python app.py` to `sh scripts/start.sh`

**What you need to do:**
1. ✅ Commit the change: `git add railway.toml && git commit -m "Fix start command"`
2. ✅ Push to GitHub: `git push origin main`
3. ✅ Wait for Railway to redeploy (~2 minutes)
4. ✅ Test the endpoints to verify

**After this fix, your deployment should work perfectly!** 🚀
