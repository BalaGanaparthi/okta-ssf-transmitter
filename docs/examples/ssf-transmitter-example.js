/**
 * SSF Transmitter Example - Send Security Event Tokens to Okta
 *
 * This example demonstrates how to:
 * 1. Generate a Security Event Token (SET)
 * 2. Sign it with RS256
 * 3. Send it to Okta as a risk signal
 */

const jwt = require('jsonwebtoken');
const axios = require('axios');
const { v4: uuidv4 } = require('uuid');
const fs = require('fs');

// ============================================================================
// Configuration
// ============================================================================

const CONFIG = {
  // Your transmitter details
  issuer: 'https://mysystem.example.com',
  privateKeyPath: './private_key.pem', // Path to your RS256 private key
  keyId: 'transmitter-key-1', // Must match the kid in your JWKS

  // Okta receiver details
  oktaDomain: 'https://your-org.okta.com',
  oktaSETEndpoint: 'https://your-org.okta.com/security/api/v1/security-events',
};

// ============================================================================
// Supported Event Types
// ============================================================================

const EVENT_TYPES = {
  CREDENTIAL_CHANGE_REQUIRED: 'https://schemas.openid.net/secevent/risc/event-type/account-credential-change-required',
  ACCOUNT_DISABLED: 'https://schemas.openid.net/secevent/risc/event-type/account-disabled',
  ACCOUNT_ENABLED: 'https://schemas.openid.net/secevent/risc/event-type/account-enabled',
};

// ============================================================================
// SET Generator
// ============================================================================

/**
 * Generate a Security Event Token (SET)
 * @param {string} eventType - One of the EVENT_TYPES
 * @param {string} userEmail - Email of the affected user in Okta
 * @param {string} reason - Human-readable reason for the event
 * @returns {string} Signed JWT (SET)
 */
function generateSET(eventType, userEmail, reason = null) {
  // Read private key
  const privateKey = fs.readFileSync(CONFIG.privateKeyPath, 'utf8');

  // Create unique event ID
  const jti = `evt_${uuidv4()}`;

  // Current timestamp
  const iat = Math.floor(Date.now() / 1000);

  // Build SET payload
  const payload = {
    iss: CONFIG.issuer,
    jti: jti,
    iat: iat,
    aud: CONFIG.oktaDomain,
    events: {}
  };

  // Add the specific event
  payload.events[eventType] = {
    subject: {
      format: 'email',
      email: userEmail
    }
  };

  // Add reason if provided
  if (reason) {
    payload.events[eventType].reason = reason;
  }

  // JWT header
  const header = {
    alg: 'RS256',
    kid: CONFIG.keyId,
    typ: 'secevent+jwt'
  };

  // Sign the SET
  const token = jwt.sign(payload, privateKey, {
    algorithm: 'RS256',
    header: header,
    noTimestamp: true // We're manually setting iat
  });

  return token;
}

// ============================================================================
// SET Transmitter
// ============================================================================

/**
 * Send a SET to Okta
 * @param {string} setToken - The signed JWT token
 * @returns {Promise<Object>} Response from Okta
 */
async function sendSET(setToken) {
  try {
    const response = await axios.post(
      CONFIG.oktaSETEndpoint,
      setToken,
      {
        headers: {
          'Content-Type': 'application/secevent+jwt'
        },
        timeout: 10000 // 10 second timeout
      }
    );

    return {
      success: true,
      status: response.status,
      data: response.data
    };
  } catch (error) {
    if (error.response) {
      // Server responded with error
      return {
        success: false,
        status: error.response.status,
        error: error.response.data
      };
    } else if (error.request) {
      // No response received
      return {
        success: false,
        error: 'No response from Okta',
        details: error.message
      };
    } else {
      // Request setup error
      return {
        success: false,
        error: 'Request failed',
        details: error.message
      };
    }
  }
}

// ============================================================================
// High-Level Functions
// ============================================================================

/**
 * Report compromised credentials for a user
 * @param {string} userEmail - User's email address
 * @param {string} reason - Why credentials are compromised
 */
async function reportCompromisedCredentials(userEmail, reason) {
  console.log(`🔒 Reporting compromised credentials for: ${userEmail}`);

  const set = generateSET(
    EVENT_TYPES.CREDENTIAL_CHANGE_REQUIRED,
    userEmail,
    reason
  );

  const result = await sendSET(set);

  if (result.success) {
    console.log(`✅ SET accepted by Okta (Status: ${result.status})`);
  } else {
    console.error(`❌ SET rejected (Status: ${result.status}):`, result.error);
  }

  return result;
}

/**
 * Request Okta to disable a user account
 * @param {string} userEmail - User's email address
 * @param {string} reason - Why account should be disabled
 */
async function disableAccount(userEmail, reason) {
  console.log(`🚫 Requesting account disable for: ${userEmail}`);

  const set = generateSET(
    EVENT_TYPES.ACCOUNT_DISABLED,
    userEmail,
    reason
  );

  const result = await sendSET(set);

  if (result.success) {
    console.log(`✅ SET accepted by Okta (Status: ${result.status})`);
  } else {
    console.error(`❌ SET rejected (Status: ${result.status}):`, result.error);
  }

  return result;
}

/**
 * Notify Okta that a previously disabled account is now safe
 * @param {string} userEmail - User's email address
 * @param {string} reason - Why account is now safe
 */
async function enableAccount(userEmail, reason) {
  console.log(`✅ Requesting account enable for: ${userEmail}`);

  const set = generateSET(
    EVENT_TYPES.ACCOUNT_ENABLED,
    userEmail,
    reason
  );

  const result = await sendSET(set);

  if (result.success) {
    console.log(`✅ SET accepted by Okta (Status: ${result.status})`);
  } else {
    console.error(`❌ SET rejected (Status: ${result.status}):`, result.error);
  }

  return result;
}

// ============================================================================
// Example Usage
// ============================================================================

async function main() {
  console.log('=== SSF Transmitter Example ===\n');

  // Example 1: Report compromised credentials
  await reportCompromisedCredentials(
    'john.doe@example.com',
    'Password found in HaveIBeenPwned database breach'
  );

  console.log('\n---\n');

  // Example 2: Disable account due to suspicious activity
  await disableAccount(
    'jane.smith@example.com',
    'Multiple failed login attempts from suspicious IP addresses'
  );

  console.log('\n---\n');

  // Example 3: Re-enable account after investigation
  await enableAccount(
    'jane.smith@example.com',
    'Investigation completed - activity confirmed as legitimate'
  );
}

// Run examples if this file is executed directly
if (require.main === module) {
  main().catch(console.error);
}

// ============================================================================
// Export for use as a module
// ============================================================================

module.exports = {
  generateSET,
  sendSET,
  reportCompromisedCredentials,
  disableAccount,
  enableAccount,
  EVENT_TYPES,
  CONFIG
};
