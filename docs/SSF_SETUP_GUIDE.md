# Okta Shared Signals Framework (SSF) Setup Guide

## Overview

### What is SSF?

The Shared Signals Framework (SSF) is an OpenID standard that enables secure communication of security events between different systems in real-time.

### Transmitter vs Receiver

- **Transmitter (Provider)**: The third-party vendor or system that SENDS security risk signals (e.g., your application detecting suspicious activity)
- **Receiver**: Okta acts as the RECEIVER, consuming these signals to take protective actions
- **Stream**: The connection between transmitter and receiver

```
┌─────────────────┐         Risk Signals          ┌─────────────┐
│   Transmitter   │ ────────────────────────────► │    Okta     │
│  (Your System)  │  (Security Event Tokens)      │  (Receiver) │
└─────────────────┘                               └─────────────┘
```

---

## Part 1: Setup Okta as SSF Receiver

### Prerequisites

1. **Okta Org**: Access to an Okta organization
2. **Identity Threat Protection**: Must be enabled (contact Okta support if not available)
3. **Admin Access**: API token with appropriate permissions
4. **Cryptographic Keys**: RS256 JWKS (JSON Web Key Set)

---

### Step 1: Generate Cryptographic Keys (JWKS)

You need to generate RSA key pairs for signing the Security Event Tokens.

**Option A: Using Online Tool**
1. Go to https://mkjwk.org/
2. Configure:
   - Key Size: 2048 bits
   - Key Use: Signature
   - Algorithm: RS256
   - Key ID: (auto-generate or provide custom)
3. Generate and download both:
   - **Public Key Set** (JWKS) - to share with Okta
   - **Private Key** - to sign your tokens (keep secure!)

**Option B: Using OpenSSL**
```bash
# Generate private key
openssl genrsa -out private_key.pem 2048

# Generate public key
openssl rsa -in private_key.pem -pubout -out public_key.pem

# Convert to JWKS format (use a tool like pem-jwk)
npm install -g pem-jwk
pem-jwk public_key.pem > jwks.json
```

**Example JWKS Structure:**
```json
{
  "keys": [
    {
      "kty": "RSA",
      "use": "sig",
      "kid": "transmitter-key-1",
      "alg": "RS256",
      "n": "xGOr-H7A-qkU...",
      "e": "AQAB"
    }
  ]
}
```

---

### Step 2: Host Your JWKS Publicly

Your JWKS must be accessible to Okta via HTTPS:

**Requirements:**
- Must return `Content-Type: application/json`
- Must be accessible via HTTPS
- Should be cached appropriately

**Options:**
1. Host on your web server at `https://yourdomain.com/.well-known/jwks.json`
2. Use cloud storage (AWS S3, Azure Blob, GCS) with public read access
3. Use a CDN for better availability

---

### Step 3: Create Okta API Token

1. Log into Okta Admin Console
2. Navigate to: **Security** → **API** → **Tokens**
3. Click **Create Token**
4. Name it (e.g., "SSF Provider Setup")
5. Copy and securely store the token (shown only once!)

---

### Step 4: Register Your System as SSF Provider in Okta

Use Okta's SSF Receiver API to register your transmitter.

**Endpoint:**
```
POST https://{yourOktaDomain}/api/v1/security-events-providers
```

**Headers:**
```
Authorization: SSWS {your-api-token}
Content-Type: application/json
```

**Request Body (Option 1 - Non-SSF Compliant):**
```json
{
  "name": "My Security System",
  "issuer": "https://mysystem.example.com",
  "jwks": {
    "keys": [
      {
        "kty": "RSA",
        "use": "sig",
        "kid": "transmitter-key-1",
        "alg": "RS256",
        "n": "xGOr-H7A...",
        "e": "AQAB"
      }
    ]
  }
}
```

**Request Body (Option 2 - SSF Compliant with Well-Known Config):**
```json
{
  "name": "My Security System",
  "wellKnownConfigurationUrl": "https://mysystem.example.com/.well-known/ssf-configuration"
}
```

**SSF Well-Known Configuration Format:**
```json
{
  "issuer": "https://mysystem.example.com",
  "jwks_uri": "https://mysystem.example.com/.well-known/jwks.json",
  "delivery_methods_supported": ["https://schemas.openid.net/secevent/risc/delivery-method/push"],
  "configuration_endpoint": "https://mysystem.example.com/ssf/stream"
}
```

**Example Response:**
```json
{
  "id": "ssp1a2b3c4d5e6f7g8h9",
  "name": "My Security System",
  "issuer": "https://mysystem.example.com",
  "status": "ACTIVE",
  "jwks": {
    "keys": [...]
  },
  "_links": {
    "self": {
      "href": "https://{yourOktaDomain}/api/v1/security-events-providers/ssp1a2b3c4d5e6f7g8h9"
    }
  }
}
```

Save the `id` from the response - you'll need it for updates/management.

---

### Step 5: Verify Provider Configuration

**List All Providers:**
```
GET https://{yourOktaDomain}/api/v1/security-events-providers
Authorization: SSWS {your-api-token}
```

**Get Specific Provider:**
```
GET https://{yourOktaDomain}/api/v1/security-events-providers/{providerId}
Authorization: SSWS {your-api-token}
```

---

### Step 6: Provider Lifecycle Management

**Update Provider:**
```
PUT https://{yourOktaDomain}/api/v1/security-events-providers/{providerId}
Content-Type: application/json
Authorization: SSWS {your-api-token}

{
  "name": "Updated Security System Name"
}
```

**Deactivate Provider:**
```
POST https://{yourOktaDomain}/api/v1/security-events-providers/{providerId}/lifecycle/deactivate
Authorization: SSWS {your-api-token}
```

**Delete Provider:**
```
DELETE https://{yourOktaDomain}/api/v1/security-events-providers/{providerId}
Authorization: SSWS {your-api-token}
```

---

## Part 2: Transmit Risk Signals to Okta

Once Okta is configured as a receiver, your system (transmitter) can send Security Event Tokens (SETs).

### Security Event Token (SET) Structure

A SET is a JWT with specific claims for security events.

**Required Components:**
1. **Header**: Algorithm and key ID
2. **Payload**: Event data and claims
3. **Signature**: RS256 signed with your private key

**SET Header:**
```json
{
  "alg": "RS256",
  "kid": "transmitter-key-1",
  "typ": "secevent+jwt"
}
```

**SET Payload:**
```json
{
  "iss": "https://mysystem.example.com",
  "jti": "unique-event-id-12345",
  "iat": 1711276800,
  "aud": "https://{yourOktaDomain}",
  "events": {
    "https://schemas.openid.net/secevent/risc/event-type/account-credential-change-required": {
      "subject": {
        "format": "email",
        "email": "user@example.com"
      },
      "reason": "Password compromised in data breach"
    }
  }
}
```

### Supported Event Types

Okta supports these RISC (Risk Incident Sharing and Coordination) event types:

1. **Account Credential Change Required**
   ```
   https://schemas.openid.net/secevent/risc/event-type/account-credential-change-required
   ```
   Use when: User credentials are compromised

2. **Account Disabled**
   ```
   https://schemas.openid.net/secevent/risc/event-type/account-disabled
   ```
   Use when: Account should be suspended

3. **Account Enabled**
   ```
   https://schemas.openid.net/secevent/risc/event-type/account-enabled
   ```
   Use when: Previously disabled account is now safe

### Sending SETs to Okta

**Endpoint:**
```
POST https://{yourOktaDomain}/security/api/v1/security-events
```

**Headers:**
```
Content-Type: application/secevent+jwt
```

**Body:**
```
eyJhbGciOiJSUzI1NiIsImtpZCI6InRyYW5zbWl0dGVyLWtleS0xIiwidHlwIjoic2VjZXZlbnQrand0In0.eyJpc3MiOiJodHRwczovL215c3lzdGVtLmV4YW1wbGUuY29tIiwianRpIjoidW5pcXVlLWV2ZW50LWlkLTEyMzQ1IiwiaWF0IjoxNzExMjc2ODAwLCJhdWQiOiJodHRwczovL3lvdXJvcmcub2t0YS5jb20iLCJldmVudHMiOnsgImh0dHBzOi8vc2NoZW1hcy5vcGVuaWQubmV0L3NlY2V2ZW50L3Jpc2MvZXZlbnQtdHlwZS9hY2NvdW50LWNyZWRlbnRpYWwtY2hhbmdlLXJlcXVpcmVkIjp7InN1YmplY3QiOnsiZm9ybWF0IjoiZW1haWwiLCJlbWFpbCI6InVzZXJAZXhhbXBsZS5jb20ifSwicmVhc29uIjoiUGFzc3dvcmQgY29tcHJvbWlzZWQifX19.signature-here
```

**Success Response (202 Accepted):**
```json
{
  "status": "accepted"
}
```

**Error Response (400 Bad Request):**
```json
{
  "error": "invalid_request",
  "error_description": "The SET is malformed or invalid"
}
```

---

## Important Requirements

### For Successful SET Transmission:

1. ✅ **Unique JTI**: Each SET must have a unique `jti` (JWT ID) claim
2. ✅ **Valid Signature**: Must be signed with RS256 using your private key
3. ✅ **Matching Issuer**: The `iss` claim must match the issuer registered in Okta
4. ✅ **Valid User**: The email subject must match an existing Okta user
5. ✅ **Correct Audience**: The `aud` claim should be your Okta domain
6. ✅ **Current Timestamp**: The `iat` (issued at) should be recent
7. ✅ **Proper Content-Type**: Must be `application/secevent+jwt`

---

## Testing Your Integration

### Test Flow:

1. **Register Provider** in Okta (Part 1)
2. **Generate a Test SET** with test user email
3. **Send SET** to Okta endpoint
4. **Verify** in Okta Admin Console:
   - Go to **Reports** → **System Log**
   - Look for security event entries
   - Check user's status if account action was triggered

### Common Issues:

| Issue | Cause | Solution |
|-------|-------|----------|
| 401 Unauthorized | Invalid/missing API token | Regenerate token, check Authorization header |
| 400 Invalid SET | Malformed JWT | Validate JWT structure, check signature |
| Issuer mismatch | SET issuer ≠ provider issuer | Ensure `iss` claim matches registered value |
| User not found | Email not in Okta | Use valid Okta user email |
| JTI duplicate | Same event ID reused | Generate unique `jti` for each SET |

---

## Next Steps

1. ✅ Review the code examples in `ssf-transmitter-example.js`
2. ✅ Import and test with `SSF_Postman_Collection.json`
3. ✅ Set up monitoring for SET transmission success/failure
4. ✅ Implement error handling and retry logic
5. ✅ Document your issuer URL and JWKS location

---

## References

- [Okta SSF Receiver Guide](https://developer.okta.com/docs/guides/configure-ssf-receiver/main/)
- [OpenID Shared Signals Framework](https://openid.net/wg/sharedsignals/)
- [RISC Event Types](https://openid.net/specs/openid-risc-profile-specification-1_0.html)
- [RFC 8417 - Security Event Token](https://datatracker.ietf.org/doc/html/rfc8417)
