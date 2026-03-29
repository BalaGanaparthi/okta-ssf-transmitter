# Certificates Directory

This directory contains the cryptographic keys used for signing Security Event Tokens (SETs).

## Files

- `private_key.pem` - RSA private key (2048-bit) used to sign JWTs
- `public_key.pem` - RSA public key that corresponds to the private key

## How It Works

1. **Private Key**
   - Used to sign Security Event Tokens (SETs)
   - Never shared with external parties
   - Stored securely on the server

2. **Public Key**
   - Exposed via the JWKS endpoint (`/.well-known/jwks.json`)
   - Used by Okta to verify the signature of your SETs
   - Safe to share publicly

## Key Generation

The application automatically generates a new RSA key pair on startup if keys don't exist.

### Manual Key Generation

If you want to generate keys manually:

```bash
# Generate private key
openssl genrsa -out private_key.pem 2048

# Extract public key
openssl rsa -in private_key.pem -pubout -out public_key.pem
```

## Security Considerations

### Development
- Keys are auto-generated and stored in this directory
- Fine for local development and testing

### Production (Railway)

**Option 1: Use Railway Volumes (Recommended)**
```
1. Add a persistent volume in Railway dashboard
2. Mount at /app/certs
3. Keys persist across deployments
```

**Option 2: Environment Variables**
```
1. Generate keys locally
2. Base64 encode them
3. Store in Railway environment variables
4. Modify app.py to decode and use them
```

**Option 3: External Key Management**
```
1. Use AWS KMS, Azure Key Vault, or similar
2. Fetch keys on startup
3. Store in memory only
```

## JWKS Format

The public key is exposed in JWKS (JSON Web Key Set) format at `/.well-known/jwks.json`:

```json
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

## Key Rotation

For production systems, implement key rotation:

1. Generate new key pair
2. Add new key to JWKS (keep old key)
3. Update Key ID in environment variables
4. Remove old key after transition period

## .gitignore

The `.pem` files in this directory should NEVER be committed to version control:

```
# In .gitignore
certs/*.pem
```

## Troubleshooting

### Keys Not Generated
- Check file permissions on the `certs/` directory
- Verify the application has write access
- Check application logs for errors

### Okta Can't Verify Signature
- Verify JWKS endpoint is publicly accessible
- Check that Key ID matches in both places:
  - Environment variable `KEY_ID`
  - JWKS `kid` field
  - JWT header `kid` field

### Permission Denied
```bash
# Fix permissions
chmod 700 certs/
chmod 600 certs/*.pem
```

## Best Practices

1. ✅ Keep private keys secure
2. ✅ Never commit keys to git
3. ✅ Use environment-specific keys
4. ✅ Rotate keys periodically
5. ✅ Monitor key usage
6. ❌ Don't share private keys
7. ❌ Don't reuse keys across environments
8. ❌ Don't expose private keys via API
