# Railway Deployment Guide

This guide walks you through deploying the SSF Transmitter web application to Railway.

## Prerequisites

1. [Railway account](https://railway.app/) (free tier available)
2. GitHub account (to connect your repository)
3. Okta organization with Identity Threat Protection enabled

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository has all the necessary files:
- `app.py` - Flask application
- `Dockerfile` - Container configuration
- `requirements.txt` - Python dependencies
- `templates/` - HTML templates
- `static/` - CSS and JavaScript files
- `.dockerignore` - Files to exclude from build

### 2. Deploy to Railway

#### Option A: Deploy from GitHub (Recommended)

1. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/ssf-transmitter.git
   git push -u origin main
   ```

2. **Connect to Railway**
   - Go to [Railway](https://railway.app/)
   - Click "Start a New Project"
   - Select "Deploy from GitHub repo"
   - Authorize Railway to access your GitHub account
   - Select your repository

3. **Railway will automatically detect the Dockerfile and deploy**

#### Option B: Deploy from CLI

1. **Install Railway CLI**
   ```bash
   npm install -g @railway/cli
   # or
   brew install railway
   ```

2. **Login to Railway**
   ```bash
   railway login
   ```

3. **Initialize and deploy**
   ```bash
   railway init
   railway up
   ```

### 3. Configure Environment Variables

After deployment, set the required environment variables in Railway:

1. Go to your project in Railway dashboard
2. Click on your service
3. Go to "Variables" tab
4. Add the following variables:

   ```
   ISSUER=https://your-app.railway.app
   OKTA_DOMAIN=https://your-org.okta.com
   KEY_ID=transmitter-key-1
   ```

   **Important:** Replace `your-app.railway.app` with your actual Railway app URL (you'll get this after deployment).

### 4. Get Your Railway URL

1. In Railway dashboard, go to "Settings" tab
2. Under "Domains", click "Generate Domain"
3. Copy your Railway URL (e.g., `https://your-app.railway.app`)

### 5. Update Environment Variables

Now that you have your Railway URL:
1. Go back to "Variables" tab
2. Update `ISSUER` with your actual Railway URL
3. Save changes

### 6. Configure Okta

#### Register Your SSF Provider in Okta

1. **Get your JWKS URL**
   - Your JWKS is available at: `https://your-app.railway.app/.well-known/jwks.json`
   - Visit this URL to verify it's accessible

2. **Register provider via Okta API**

   Use the following curl command or Postman:

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

   Or use the Okta Admin Console (if available in your org).

### 7. Test Your Deployment

1. **Access your app**
   - Visit `https://your-app.railway.app`
   - You should see the SSF Transmitter UI

2. **Send a test event**
   - Enter a test user email (must exist in Okta)
   - Select an event type
   - Add a reason
   - Click "Send Security Event"

3. **Verify in Okta**
   - Go to Okta Admin Console
   - Navigate to Reports → System Log
   - Look for security event entries

### 8. Monitor Your Application

Railway provides built-in monitoring:

1. **View Logs**
   - In Railway dashboard, go to "Deployments" tab
   - Click on a deployment to view logs

2. **Health Check**
   - Visit `https://your-app.railway.app/health`
   - Should return `{"status": "healthy"}`

3. **JWKS Endpoint**
   - Visit `https://your-app.railway.app/.well-known/jwks.json`
   - Should return your public key in JWKS format

## Troubleshooting

### Application Won't Start

1. **Check logs in Railway dashboard**
   ```
   Deployments → Latest deployment → View logs
   ```

2. **Verify environment variables are set correctly**
   - ISSUER should be your Railway URL
   - OKTA_DOMAIN should be your Okta org URL

### JWKS Endpoint Not Accessible

1. **Verify deployment is successful**
   - Check deployment status in Railway dashboard

2. **Test the endpoint**
   ```bash
   curl https://your-app.railway.app/.well-known/jwks.json
   ```

### Events Not Being Received by Okta

1. **Check provider registration**
   - Verify issuer matches exactly
   - Verify JWKS URL is accessible

2. **Check Okta System Log**
   - Look for validation errors
   - Check for signature verification issues

3. **Verify user exists**
   - The user email must exist in your Okta org

### Port Issues

Railway automatically sets the `PORT` environment variable. The application is configured to use it, but if you have issues:

1. Check that `PORT` is not overridden in your environment variables
2. Railway expects your app to listen on `0.0.0.0:$PORT`

## Security Considerations

### Certificate Management

The application automatically generates RSA key pairs on first startup. These keys are stored in the `certs/` folder inside the container.

**Important:**
- Keys are regenerated on each deployment
- For production, consider using Railway's persistent volumes or external key management
- Keep your private keys secure and never commit them to version control

### To use persistent keys:

1. **Option A: Use Railway Volumes (Recommended)**
   - In Railway dashboard, go to your service
   - Add a volume mounted at `/app/certs`
   - Keys will persist across deployments

2. **Option B: Provide keys via environment variables**
   - Store base64-encoded keys in environment variables
   - Modify `app.py` to decode and use them

## Scaling

Railway provides automatic scaling:

1. **Horizontal Scaling**
   - Not needed for most SSF use cases
   - Each instance can handle thousands of events

2. **Vertical Scaling**
   - Upgrade your Railway plan for more resources
   - Free tier is sufficient for development/testing

## Cost Optimization

1. **Free Tier**
   - Railway offers $5 credit per month (free tier)
   - Sufficient for testing and small-scale production

2. **Usage-based Pricing**
   - Charged for CPU and memory usage
   - This lightweight app typically costs $1-2/month

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Configure environment variables
3. ✅ Register provider in Okta
4. ✅ Test sending events
5. 📚 Review [SSF_SETUP_GUIDE.md](SSF_SETUP_GUIDE.md) for Okta configuration details
6. 🔄 Set up CI/CD (optional)

## Support

- Railway Documentation: https://docs.railway.app/
- Okta SSF Documentation: https://developer.okta.com/docs/guides/configure-ssf-receiver/
- GitHub Issues: [Your repository issues page]

## Additional Resources

- [Dockerfile best practices](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)
- [Flask deployment guide](https://flask.palletsprojects.com/en/3.0.x/deploying/)
- [OpenID Shared Signals](https://openid.net/wg/sharedsignals/)
