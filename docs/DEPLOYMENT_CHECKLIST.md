# Deployment Checklist

Use this checklist to ensure a successful deployment to Railway.

## Pre-Deployment

### Local Testing
- [ ] Application runs locally without errors
- [ ] All dependencies in `requirements.txt` are correct
- [ ] `.env` file configured with test values
- [ ] Health endpoint (`/health`) returns 200
- [ ] JWKS endpoint (`/.well-known/jwks.json`) returns valid JSON
- [ ] UI loads correctly in browser
- [ ] Can send test events through UI

### Code Repository
- [ ] Code pushed to GitHub/GitLab
- [ ] `.gitignore` configured (no `.pem` files committed)
- [ ] `README_WEB_APP.md` reviewed
- [ ] `RAILWAY_DEPLOYMENT.md` reviewed

### Okta Prerequisites
- [ ] Okta organization with Identity Threat Protection enabled
- [ ] Okta API token generated
- [ ] Test user account exists in Okta
- [ ] Okta domain URL confirmed

## Railway Deployment

### Initial Setup
- [ ] Railway account created
- [ ] Railway CLI installed (optional)
- [ ] Repository connected to Railway
- [ ] Service created in Railway project

### Environment Variables
Set these in Railway dashboard under "Variables":

- [ ] `ISSUER` = `https://your-app.railway.app`
  - ⚠️ Update after getting Railway URL
- [ ] `OKTA_DOMAIN` = `https://your-org.okta.com`
  - Replace with your actual Okta org
- [ ] `KEY_ID` = `transmitter-key-1`
  - Or your custom key ID

### Deployment
- [ ] Initial deployment triggered
- [ ] Build completed successfully
- [ ] Container started without errors
- [ ] Railway domain generated
- [ ] Custom domain configured (optional)

### Post-Deployment
- [ ] Update `ISSUER` variable with actual Railway URL
- [ ] Redeploy after updating environment variables
- [ ] Application accessible at Railway URL
- [ ] Health check returns 200
- [ ] JWKS endpoint publicly accessible

## Okta Configuration

### Register SSF Provider
- [ ] JWKS URL confirmed: `https://your-app.railway.app/.well-known/jwks.json`
- [ ] Provider registered via Okta API or Admin Console
- [ ] Provider name: "SSF Transmitter"
- [ ] Issuer URL matches `ISSUER` environment variable exactly
- [ ] JWKS URL accessible from Okta (no firewall blocks)

### Verification
```bash
# Register provider (replace with your values)
curl -X POST "https://your-org.okta.com/api/v1/security/api/v1/security-events-providers" \
  -H "Authorization: SSWS YOUR_OKTA_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "SSF Transmitter",
    "issuer": "https://your-app.railway.app",
    "jwks_url": "https://your-app.railway.app/.well-known/jwks.json"
  }'
```

- [ ] Provider registration successful
- [ ] Provider appears in Okta Admin Console (if available)

## Testing

### Functional Tests
- [ ] Access Railway URL in browser
- [ ] UI loads correctly
- [ ] Configuration displayed correctly
- [ ] Event type dropdown populated
- [ ] Can submit form without errors

### Integration Tests
- [ ] Send test event for `CREDENTIAL_CHANGE_REQUIRED`
- [ ] Send test event for `ACCOUNT_DISABLED`
- [ ] Send test event for `ACCOUNT_ENABLED`
- [ ] Check Okta System Log for events
- [ ] Verify events have correct status (accepted/rejected)

### Error Handling
- [ ] Test with invalid email format
- [ ] Test with non-existent user
- [ ] Test with missing required fields
- [ ] Error messages display correctly

## Production Readiness

### Security
- [ ] Private keys never committed to repository
- [ ] Environment variables set correctly
- [ ] HTTPS enabled (Railway provides this)
- [ ] No sensitive data in logs
- [ ] Rate limiting considered (if needed)

### Monitoring
- [ ] Railway logs accessible
- [ ] Health check endpoint monitored
- [ ] Error alerts configured (optional)
- [ ] Usage metrics reviewed

### Documentation
- [ ] Team members trained on usage
- [ ] Okta admin contact identified
- [ ] Incident response plan created (optional)
- [ ] User guide distributed

## Optional Enhancements

### Persistence
- [ ] Railway volume added for persistent keys
- [ ] Keys backed up securely
- [ ] Key rotation plan documented

### Scaling
- [ ] Resource limits reviewed
- [ ] Auto-scaling configured (if needed)
- [ ] Performance benchmarks established

### CI/CD
- [ ] GitHub Actions workflow created (optional)
- [ ] Automated tests on pull requests
- [ ] Automatic deployment on merge to main

### Monitoring & Alerts
- [ ] Logging solution integrated (optional)
- [ ] Error tracking (Sentry, etc.) configured
- [ ] Uptime monitoring (UptimeRobot, etc.) enabled
- [ ] Slack/email alerts configured

## Post-Launch

### Day 1
- [ ] Monitor logs for errors
- [ ] Test with real users
- [ ] Verify events reaching Okta
- [ ] Check response times

### Week 1
- [ ] Review usage patterns
- [ ] Optimize as needed
- [ ] Gather user feedback
- [ ] Document any issues

### Month 1
- [ ] Review security posture
- [ ] Consider key rotation
- [ ] Update documentation
- [ ] Plan improvements

## Troubleshooting Checklist

If something goes wrong:

### Application Issues
- [ ] Check Railway deployment logs
- [ ] Verify environment variables are set
- [ ] Check health endpoint status
- [ ] Review recent code changes
- [ ] Restart application

### Okta Integration Issues
- [ ] Verify provider registration
- [ ] Check JWKS URL accessibility
- [ ] Confirm issuer URL matches exactly
- [ ] Review Okta system logs
- [ ] Verify user exists in Okta

### Network Issues
- [ ] Check Railway service status
- [ ] Verify DNS resolution
- [ ] Test JWKS endpoint from external location
- [ ] Check firewall rules (if applicable)

## Support Resources

- Railway Dashboard: https://railway.app/dashboard
- Railway Docs: https://docs.railway.app/
- Okta Developer Docs: https://developer.okta.com/
- Project Documentation:
  - [README_WEB_APP.md](README_WEB_APP.md)
  - [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)
  - [SSF_SETUP_GUIDE.md](SSF_SETUP_GUIDE.md)

## Success Criteria

✅ **Deployment is successful when:**
1. Application accessible at Railway URL
2. Health check returns 200
3. JWKS endpoint returns valid JSON
4. UI loads and functions correctly
5. Test events sent to Okta successfully
6. Events appear in Okta system logs
7. No errors in Railway logs

---

**Last Updated:** [Date]
**Deployed By:** [Name]
**Railway URL:** [URL]
**Okta Org:** [Okta Domain]
