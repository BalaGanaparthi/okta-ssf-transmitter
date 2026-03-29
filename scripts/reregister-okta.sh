#!/bin/bash
# Quick script to re-register SSF provider with Okta

echo "╔══════════════════════════════════════════════════════════════╗"
echo "║       Re-register SSF Provider with Okta                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""

# Check if required variables are set
if [ -z "$OKTA_DOMAIN" ] || [ -z "$OKTA_API_TOKEN" ] || [ -z "$RAILWAY_URL" ]; then
    echo "❌ Required environment variables not set!"
    echo ""
    echo "Please set these variables first:"
    echo ""
    echo "  export OKTA_DOMAIN=\"https://your-org.okta.com\""
    echo "  export OKTA_API_TOKEN=\"your-okta-api-token\""
    echo "  export RAILWAY_URL=\"https://your-app.railway.app\""
    echo ""
    echo "Then run this script again."
    exit 1
fi

echo "Configuration:"
echo "  Okta Domain: $OKTA_DOMAIN"
echo "  Railway URL: $RAILWAY_URL"
echo ""

# Step 1: Verify JWKS is accessible
echo "Step 1: Verifying JWKS endpoint..."
JWKS_URL="$RAILWAY_URL/.well-known/jwks.json"

if curl -s -f "$JWKS_URL" > /dev/null; then
    echo "✅ JWKS endpoint is accessible"
    echo "   URL: $JWKS_URL"
else
    echo "❌ JWKS endpoint is NOT accessible!"
    echo "   URL: $JWKS_URL"
    echo ""
    echo "Please ensure your Railway deployment is running."
    exit 1
fi

echo ""

# Step 2: List existing providers
echo "Step 2: Checking for existing SSF Transmitter provider..."
PROVIDERS=$(curl -s -X GET "$OKTA_DOMAIN/api/v1/security/api/v1/security-events-providers" \
  -H "Authorization: SSWS $OKTA_API_TOKEN" \
  -H "Accept: application/json")

# Check if response is valid JSON
if echo "$PROVIDERS" | jq empty 2>/dev/null; then
    # Valid JSON - check if it's an error
    if echo "$PROVIDERS" | jq -e '.errorCode' > /dev/null 2>&1; then
        echo "❌ Okta API Error:"
        echo "$PROVIDERS" | jq '.'
        echo ""
        echo "Common issues:"
        echo "  - Invalid API token"
        echo "  - Wrong Okta domain"
        echo "  - Missing permissions"
        echo "  - SSF feature not enabled"
        exit 1
    fi

    # Find existing provider
    PROVIDER_ID=$(echo "$PROVIDERS" | jq -r '.[] | select(.name=="SSF Transmitter") | .id' 2>/dev/null | head -1)

    if [ -n "$PROVIDER_ID" ]; then
        echo "✅ Found existing provider: $PROVIDER_ID"
        echo ""
        read -p "Do you want to DELETE the old provider and re-register? (y/n) " -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo ""
            echo "Step 3: Deleting old provider..."
            DELETE_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X DELETE \
                "$OKTA_DOMAIN/api/v1/security/api/v1/security-events-providers/$PROVIDER_ID" \
                -H "Authorization: SSWS $OKTA_API_TOKEN")

            HTTP_CODE=$(echo "$DELETE_RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)

            if [ "$HTTP_CODE" = "204" ] || [ "$HTTP_CODE" = "200" ]; then
                echo "✅ Old provider deleted"
            else
                echo "⚠️  Delete returned: $HTTP_CODE"
            fi
            echo ""
        fi
    else
        echo "ℹ️  No existing provider found"
        echo ""
    fi
else
    echo "❌ Invalid response from Okta API"
    echo "Response: $PROVIDERS"
    echo ""
    echo "Please check:"
    echo "  - OKTA_DOMAIN is correct (e.g., https://your-org.okta.com)"
    echo "  - OKTA_API_TOKEN is valid"
    exit 1
fi

# Step 4: Register new provider
echo "Step 4: Registering new provider..."
REGISTER_RESPONSE=$(curl -s -w "\nHTTP_STATUS:%{http_code}" -X POST \
    "$OKTA_DOMAIN/api/v1/security/api/v1/security-events-providers" \
    -H "Authorization: SSWS $OKTA_API_TOKEN" \
    -H "Content-Type: application/json" \
    -H "Accept: application/json" \
    -d '{
      "name": "SSF Transmitter",
      "issuer": "'"$RAILWAY_URL"'",
      "jwks_url": "'"$JWKS_URL"'"
    }')

HTTP_CODE=$(echo "$REGISTER_RESPONSE" | grep "HTTP_STATUS:" | cut -d: -f2)
RESPONSE_BODY=$(echo "$REGISTER_RESPONSE" | grep -v "HTTP_STATUS:")

if [ "$HTTP_CODE" = "200" ] || [ "$HTTP_CODE" = "201" ]; then
    echo "✅ Provider registered successfully!"
    echo ""
    echo "Provider Details:"
    echo "$RESPONSE_BODY" | jq '.'

    NEW_PROVIDER_ID=$(echo "$RESPONSE_BODY" | jq -r '.id' 2>/dev/null)
    if [ -n "$NEW_PROVIDER_ID" ] && [ "$NEW_PROVIDER_ID" != "null" ]; then
        echo ""
        echo "📝 Provider ID: $NEW_PROVIDER_ID"
        echo "📝 Save this ID for future reference"
    fi
else
    echo "❌ Registration failed with HTTP $HTTP_CODE"
    echo ""
    echo "Response:"
    echo "$RESPONSE_BODY" | jq '.' 2>/dev/null || echo "$RESPONSE_BODY"
    exit 1
fi

echo ""
echo "╔══════════════════════════════════════════════════════════════╗"
echo "║                    Registration Complete!                     ║"
echo "╚══════════════════════════════════════════════════════════════╝"
echo ""
echo "Next steps:"
echo "  1. Wait 1-2 minutes for Okta to cache the new JWKS"
echo "  2. Test sending an event"
echo "  3. Verify in Okta System Log"
echo ""
echo "Test command:"
echo "  curl -X POST $RAILWAY_URL/api/send-event \\"
echo "    -H \"Content-Type: application/json\" \\"
echo "    -d '{\"subject\":\"test@example.com\",\"eventType\":\"CREDENTIAL_CHANGE_REQUIRED\",\"reason\":\"Test\"}'"
echo ""
