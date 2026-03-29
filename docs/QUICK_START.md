# Quick Start Guide 🚀

Get your SSF Transmitter up and running in minutes!

## 🏃 Super Quick Start

### Local (3 commands)
```bash
./run.sh
# Open http://localhost:8080
# Start sending events!
```

### Railway (3 steps)
1. Push to GitHub
2. Connect to Railway
3. Set environment variables ✅

## 📋 What You Need

### For Local Testing:
- Python 3.9+
- Terminal

### For Railway Deployment:
- GitHub account
- Railway account (free tier OK)
- Okta organization

## 🎯 Step-by-Step

### Local Development

**1. Clone & Setup**
```bash
cd project005-SSF
./run.sh
```

**2. Configure Environment**
Edit `.env` (created automatically):
```env
ISSUER=http://localhost:8080
OKTA_DOMAIN=https://your-org.okta.com
KEY_ID=transmitter-key-1
```

**3. Access UI**
Open browser: http://localhost:8080

**4. Test JWKS**
Visit: http://localhost:8080/.well-known/jwks.json

### Railway Deployment

**1. Prepare Repository**
```bash
git init
git add .
git commit -m "SSF Transmitter ready for Railway"
git remote add origin https://github.com/yourusername/ssf-transmitter.git
git push -u origin main
```

**2. Deploy to Railway**
- Go to https://railway.app/
- Click "New Project"
- Select "Deploy from GitHub"
- Choose your repository
- Wait for build ⏳

**3. Set Environment Variables**
In Railway dashboard → Variables:
```
ISSUER=https://your-app.railway.app
OKTA_DOMAIN=https://your-org.okta.com
KEY_ID=transmitter-key-1
```

**4. Get Your URL**
- Settings → Generate Domain
- Copy URL (e.g., `your-app.railway.app`)
- Update `ISSUER` variable with this URL
- Redeploy

**5. Register with Okta**
```bash
curl -X POST "https://your-org.okta.com/api/v1/security/api/v1/security-events-providers" \
  -H "Authorization: SSWS YOUR_OKTA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SSF Transmitter",
    "issuer": "https://your-app.railway.app",
    "jwks_url": "https://your-app.railway.app/.well-known/jwks.json"
  }'
```

**6. Test!**
- Visit your Railway URL
- Fill in the form
- Send a test event
- Check Okta System Log

## 🎨 Using the UI

### Send an Event

1. **Enter User Email**
   - Must be an existing Okta user
   - Format: `user@example.com`

2. **Select Event Type**
   - Credential Change Required
   - Account Disabled
   - Account Enabled

3. **Add Reason (Optional)**
   - Explain why the event is happening
   - e.g., "Password found in breach"

4. **Click Send**
   - Watch for success/error message
   - Check response details

### Event Types Explained

**🔒 Credential Change Required**
Use when: User credentials compromised
Result: Okta may force password reset

**🚫 Account Disabled**
Use when: Suspicious activity detected
Result: Okta may suspend account

**✅ Account Enabled**
Use when: False alarm resolved
Result: Okta may re-enable account

## ✅ Verification

### Check Everything Works

**1. Health Check**
```bash
curl http://localhost:8080/health
# Should return: {"status": "healthy"}
```

**2. JWKS Endpoint**
```bash
curl http://localhost:8080/.well-known/jwks.json | jq
# Should return JSON with RSA public key
```

**3. Configuration**
```bash
curl http://localhost:8080/api/config | jq
# Should return your configuration
```

**4. Event Types**
```bash
curl http://localhost:8080/api/event-types | jq
# Should return all event types
```

## 🐛 Troubleshooting

### Application Won't Start
```bash
# Check Python version
python3 --version  # Need 3.9+

# Reinstall dependencies
pip install -r requirements.txt

# Check port availability
lsof -i :8080
```

### JWKS Not Working
```bash
# Check keys exist
ls -la certs/

# Regenerate keys
rm certs/*.pem
python app.py  # Will regenerate
```

### Events Not Reaching Okta
1. Check provider registered in Okta
2. Verify JWKS URL publicly accessible
3. Confirm user exists in Okta
4. Review Okta system logs

### Railway Deployment Fails
1. Check build logs in Railway dashboard
2. Verify Dockerfile syntax
3. Ensure all files committed to git
4. Check environment variables set

## 📊 Testing Events

### Test with cURL

```bash
curl -X POST http://localhost:8080/api/send-event \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "test@example.com",
    "eventType": "CREDENTIAL_CHANGE_REQUIRED",
    "reason": "Testing SSF integration"
  }'
```

### Expected Success Response
```json
{
  "success": true,
  "status": 202,
  "data": {
    "message": "Event accepted"
  }
}
```

### Expected Error Response
```json
{
  "success": false,
  "status": 400,
  "error": {
    "errorCode": "E0000001",
    "errorSummary": "User not found"
  }
}
```

## 🎯 Next Steps

After getting it running:

1. **Read Full Docs**
   - [README_WEB_APP.md](README_WEB_APP.md) - Complete guide
   - [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md) - Deployment details
   - [SSF_SETUP_GUIDE.md](SSF_SETUP_GUIDE.md) - Okta setup

2. **Review Checklist**
   - [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Step-by-step

3. **Configure Okta**
   - Enable Identity Threat Protection
   - Generate API token
   - Register SSF provider

4. **Test Integration**
   - Send test events
   - Verify in Okta logs
   - Test all event types

## 💡 Pro Tips

- 🔑 **Keys auto-generate** - No manual setup needed
- 🌍 **ISSUER must be public** - Railway URL works
- 📧 **User must exist** - Test with real Okta users
- 🔄 **Update ISSUER** - After Railway gives you URL
- 📊 **Check Okta logs** - Reports → System Log
- 🧪 **Test locally first** - Before deploying

## 🆘 Help

Stuck? Check these:
- [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) - What was built
- [DEPLOYMENT_CHECKLIST.md](DEPLOYMENT_CHECKLIST.md) - Deployment steps
- Railway logs - Deployment → View logs
- Okta logs - Reports → System Log

## 🎉 Success!

You should now have:
- ✅ Application running
- ✅ Beautiful UI accessible
- ✅ JWKS endpoint working
- ✅ Ready to send events

**Start sending security events to Okta!** 🚀

---

Need more help? See the full documentation in the project files.
