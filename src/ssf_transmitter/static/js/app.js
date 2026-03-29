// State
let eventTypes = {};
let config = {};

// Initialize
document.addEventListener('DOMContentLoaded', async () => {
    await loadConfig();
    await loadEventTypes();
    setupEventListeners();
});

// Load configuration
async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        config = await response.json();
        displayConfig();
    } catch (error) {
        console.error('Failed to load config:', error);
        showNotification('Failed to load configuration', 'error');
    }
}

// Load event types
async function loadEventTypes() {
    try {
        const response = await fetch('/api/event-types');
        eventTypes = await response.json();
        populateEventTypes();
    } catch (error) {
        console.error('Failed to load event types:', error);
        showNotification('Failed to load event types', 'error');
    }
}

// Populate event type dropdown with categories
function populateEventTypes() {
    const select = document.getElementById('eventType');

    // Group events by category
    const categories = {};
    Object.keys(eventTypes).forEach(key => {
        const event = eventTypes[key];
        const category = event.category || 'Other';

        if (!categories[category]) {
            categories[category] = [];
        }

        categories[category].push({
            key: key,
            label: event.label,
            deprecated: event.deprecated || false
        });
    });

    // Sort categories
    const sortedCategories = Object.keys(categories).sort();

    // Add optgroups for each category
    sortedCategories.forEach(category => {
        const optgroup = document.createElement('optgroup');
        optgroup.label = category;

        // Sort events within category
        categories[category].sort((a, b) => a.label.localeCompare(b.label));

        categories[category].forEach(event => {
            const option = document.createElement('option');
            option.value = event.key;
            option.textContent = event.label;

            // Add visual indicator for deprecated events
            if (event.deprecated) {
                option.textContent += ' ⚠️';
                option.style.color = '#f59e0b';
            }

            optgroup.appendChild(option);
        });

        select.appendChild(optgroup);
    });
}

// Display configuration
function displayConfig() {
    const configGrid = document.getElementById('configGrid');
    configGrid.innerHTML = '';

    const configItems = [
        { label: 'Issuer', value: config.issuer },
        { label: 'Okta Domain', value: config.oktaDomain },
        { label: 'Key ID', value: config.keyId },
        { label: 'JWKS URL', value: config.jwksUrl }
    ];

    configItems.forEach(item => {
        const div = document.createElement('div');
        div.className = 'config-item';
        div.innerHTML = `
            <span class="config-label">${item.label}</span>
            <span class="config-value">${item.value}</span>
        `;
        configGrid.appendChild(div);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Form submission
    document.getElementById('eventForm').addEventListener('submit', handleSubmit);

    // Event type change
    document.getElementById('eventType').addEventListener('change', handleEventTypeChange);

    // Close response
    document.getElementById('closeResponse').addEventListener('click', () => {
        document.getElementById('responseCard').style.display = 'none';
    });
}

// Handle event type change
function handleEventTypeChange(e) {
    const eventType = e.target.value;
    const description = document.getElementById('eventDescription');
    const dynamicFields = document.getElementById('dynamicFields');
    const reasonFieldGroup = document.getElementById('reasonFieldGroup');

    if (eventType && eventTypes[eventType]) {
        description.textContent = eventTypes[eventType].description;
        description.classList.add('show');

        // Clear dynamic fields
        dynamicFields.innerHTML = '';

        // Generate fields dynamically based on field_definitions
        const fieldDefinitions = eventTypes[eventType].field_definitions || [];
        let hasReasonField = false;

        if (fieldDefinitions.length > 0) {
            fieldDefinitions.forEach(field => {
                if (field.name === 'reason') {
                    hasReasonField = true;
                }
                const fieldHtml = generateFieldHtml(field);
                if (fieldHtml) {
                    dynamicFields.innerHTML += fieldHtml;
                }
            });
        }

        // Hide general reason field if event has specific reason field
        if (hasReasonField) {
            reasonFieldGroup.style.display = 'none';
        } else {
            reasonFieldGroup.style.display = 'block';
        }
    } else {
        description.classList.remove('show');
        dynamicFields.innerHTML = '';
        reasonFieldGroup.style.display = 'block';
    }
}

// Generate HTML for a form field based on its schema
function generateFieldHtml(field) {
    const required = field.required ? 'required' : '';
    const requiredLabel = field.required ? '*' : '';
    const requiredHint = field.required ? '(REQUIRED)' : '(Optional)';
    const fieldId = field.name.replace(/-/g, '_').replace(/\./g, '_');

    // Icon for input fields
    const iconSvg = `
        <svg class="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 3.33333V16.6667M10 16.6667L15 11.6667M10 16.6667L5 11.6667" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
    `;

    let inputHtml = '';

    // Generate input based on field type
    if (field.type === 'select' && field.options) {
        // Dropdown field
        const optionsHtml = field.options.map(opt =>
            `<option value="${opt.value}">${opt.label}</option>`
        ).join('');

        inputHtml = `
            <div class="form-group">
                <label for="${fieldId}">
                    <span class="label-text">${field.label} ${requiredLabel}</span>
                    <span class="label-hint">${field.hint} ${requiredHint}</span>
                </label>
                <div class="select-wrapper">
                    ${iconSvg}
                    <select id="${fieldId}" name="${field.name}" ${required}>
                        <option value="">${field.placeholder || 'Select...'}</option>
                        ${optionsHtml}
                    </select>
                </div>
            </div>
        `;
    } else if (field.type === 'datetime-local') {
        // Datetime field - set default to current time
        const now = new Date();
        const year = now.getFullYear();
        const month = String(now.getMonth() + 1).padStart(2, '0');
        const day = String(now.getDate()).padStart(2, '0');
        const hours = String(now.getHours()).padStart(2, '0');
        const minutes = String(now.getMinutes()).padStart(2, '0');
        const defaultValue = `${year}-${month}-${day}T${hours}:${minutes}`;

        inputHtml = `
            <div class="form-group">
                <label for="${fieldId}">
                    <span class="label-text">${field.label} ${requiredLabel}</span>
                    <span class="label-hint">${field.hint} ${requiredHint}</span>
                </label>
                <div class="input-wrapper">
                    ${iconSvg}
                    <input type="datetime-local" id="${fieldId}" name="${field.name}" value="${defaultValue}" ${required}>
                </div>
                <div style="margin-top: 0.25rem; font-size: 0.75rem; color: var(--text-secondary); padding-left: 2.5rem;">
                    💡 Will be converted to Unix timestamp before sending to Okta
                </div>
            </div>
        `;
    } else {
        // Text input field
        inputHtml = `
            <div class="form-group">
                <label for="${fieldId}">
                    <span class="label-text">${field.label} ${requiredLabel}</span>
                    <span class="label-hint">${field.hint} ${requiredHint}</span>
                </label>
                <div class="input-wrapper">
                    ${iconSvg}
                    <input type="text" id="${fieldId}" name="${field.name}" placeholder="${field.placeholder || ''}" ${required}>
                </div>
            </div>
        `;
    }

    return inputHtml;
}

// Handle form submission
async function handleSubmit(e) {
    e.preventDefault();

    const submitBtn = document.getElementById('submitBtn');
    const btnText = submitBtn.querySelector('.btn-text');
    const btnIcon = submitBtn.querySelector('.btn-icon');

    // Get form data
    const formData = {
        subject: document.getElementById('subject').value,
        eventType: document.getElementById('eventType').value
    };

    // Get general reason field (if visible)
    const reasonText = document.getElementById('reasonText').value;
    if (reasonText && document.getElementById('reasonFieldGroup').style.display !== 'none') {
        formData.reason = reasonText;
    }

    // Validate basic fields
    if (!formData.subject || !formData.eventType) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }

    // Dynamically collect all extra fields for this event type
    const eventTypeData = eventTypes[formData.eventType];
    if (eventTypeData && eventTypeData.field_definitions) {
        console.log('Event type data:', eventTypeData);
        console.log('Field definitions:', eventTypeData.field_definitions);

        for (const field of eventTypeData.field_definitions) {
            const fieldId = field.name.replace(/-/g, '_').replace(/\./g, '_');
            const element = document.getElementById(fieldId);

            console.log(`Collecting field: ${field.name}, ID: ${fieldId}, Element:`, element);

            if (element) {
                const value = element.value;
                console.log(`  Value: ${value}`);

                // Check if required field is empty
                if (field.required && !value) {
                    showNotification(`${field.label} is required for this event type`, 'error');
                    return;
                }

                // Add to formData if has value
                if (value) {
                    formData[field.name] = value;
                    console.log(`  Added to formData: ${field.name} = ${value}`);
                }
            } else {
                console.log(`  Element not found!`);
            }
        }
    }

    console.log('Final formData to send:', formData);

    // Debug: First send to debug endpoint to see what we're sending
    if (window.location.search.includes('debug')) {
        console.log('Debug mode: sending to debug endpoint');
        try {
            const debugResponse = await fetch('/api/debug-event', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(formData)
            });
            const debugData = await debugResponse.json();
            console.log('Debug response:', debugData);
            alert('Debug mode - check console for details');
            return;
        } catch (e) {
            console.error('Debug error:', e);
        }
    }

    // Disable button and show loading
    submitBtn.disabled = true;
    btnIcon.style.display = 'none';
    btnText.textContent = 'Sending...';
    const spinner = document.createElement('div');
    spinner.className = 'spinner';
    submitBtn.appendChild(spinner);

    try {
        const response = await fetch('/api/send-event', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        });

        const result = await response.json();

        // Show response
        displayResponse(result);

        // Reset form if successful
        if (result.success) {
            document.getElementById('eventForm').reset();
            document.getElementById('eventDescription').classList.remove('show');
            showNotification('Security event sent successfully!', 'success');
        } else {
            showNotification('Failed to send security event', 'error');
        }

    } catch (error) {
        console.error('Error sending event:', error);
        displayResponse({
            success: false,
            error: 'Network error',
            details: error.message
        });
        showNotification('Failed to send security event', 'error');
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        btnText.textContent = 'Send Security Event';
        spinner.remove();
        btnIcon.style.display = 'block';
    }
}

// Display response
function displayResponse(result) {
    const responseCard = document.getElementById('responseCard');
    const responseContent = document.getElementById('responseContent');

    let html = '';

    if (result.success) {
        html = `
            <div class="response-success">
                <span class="response-label">✅ Success</span>
                <p>Security event sent successfully to Okta.</p>
                ${result.status ? `<p style="margin-top: 0.5rem;"><strong>Status:</strong> ${result.status}</p>` : ''}
                ${result.okta_endpoint ? `<p><strong>Endpoint:</strong> <code style="font-size: 0.75rem;">${result.okta_endpoint}</code></p>` : ''}
                ${result.transmission_time ? `<p><strong>Transmission Time:</strong> ${result.transmission_time.toFixed(2)}s</p>` : ''}
                ${result.data ? `<div class="response-data">${JSON.stringify(result.data, null, 2)}</div>` : ''}
                <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.1); border-left: 3px solid var(--success); border-radius: 8px; font-size: 0.875rem;">
                    ℹ️ <strong>Event logged in Okta:</strong> Check Reports → System Log in Okta Admin Console
                </div>
            </div>
        `;

        // Add JWT details if available
        if (result.jwt_token) {
            html += generateJwtDisplay(result);
        }
    } else {
        html = `
            <div class="response-error">
                <span class="response-label">❌ Error</span>
                ${result.status ? `<p><strong>Status:</strong> ${result.status}</p>` : ''}
                ${result.okta_endpoint ? `<p><strong>Endpoint:</strong> <code style="font-size: 0.75rem;">${result.okta_endpoint}</code></p>` : ''}
                ${result.transmission_time ? `<p><strong>Transmission Time:</strong> ${result.transmission_time.toFixed(2)}s</p>` : ''}
                ${result.error ? `<p><strong>Error:</strong> ${typeof result.error === 'object' ? JSON.stringify(result.error) : result.error}</p>` : ''}
                ${result.details ? `<p><strong>Details:</strong> ${result.details}</p>` : ''}
                ${result.error && typeof result.error === 'object' ? `<div class="response-data">${JSON.stringify(result.error, null, 2)}</div>` : ''}
                ${result.okta_response ? `
                    <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(239, 68, 68, 0.1); border-left: 3px solid var(--error); border-radius: 8px; font-size: 0.875rem;">
                        <strong>⚠️ Why this error occurred:</strong><br>
                        The SET was transmitted to Okta, but Okta rejected it due to validation errors.<br><br>
                        <strong>Note:</strong> Rejected events do NOT appear in Okta System Log. Only successfully accepted events (status 202) are logged by Okta.<br><br>
                        Check the JWT Payload below to verify all required fields are present with correct names.
                    </div>
                ` : ''}
            </div>
        `;

        // Add JWT details even for errors (to debug)
        if (result.jwt_token) {
            html += generateJwtDisplay(result);
        }
    }

    responseContent.innerHTML = html;
    responseCard.style.display = 'block';

    // Setup JWT.io button click handler
    const jwtButton = document.getElementById('openJwtIo');
    if (jwtButton && result.jwt_token) {
        jwtButton.addEventListener('click', () => {
            openInJwtIo(result.jwt_token);
        });
    }

    // Setup copy button click handlers
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const text = e.target.dataset.copy;
            navigator.clipboard.writeText(text).then(() => {
                e.target.textContent = '✓ Copied!';
                setTimeout(() => {
                    e.target.textContent = 'Copy';
                }, 2000);
            });
        });
    });

    // Scroll to response
    responseCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

// Generate JWT display HTML
function generateJwtDisplay(result) {
    const jwtToken = result.jwt_token;
    const jwtPayload = result.jwt_payload;
    const jwtHeader = result.jwt_header;

    // Truncate token for display
    const tokenStart = jwtToken.substring(0, 50);
    const tokenEnd = jwtToken.substring(jwtToken.length - 50);

    return `
        <div style="margin-top: 1.5rem; padding-top: 1.5rem; border-top: 1px solid rgba(148, 163, 184, 0.1);">
            <h4 style="margin-bottom: 1rem; font-size: 1rem; font-weight: 600;">📋 JWT Details</h4>

            <!-- JWT Token -->
            <div style="margin-bottom: 1rem;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
                    <strong style="font-size: 0.875rem;">Token:</strong>
                    <div style="display: flex; gap: 0.5rem;">
                        <button class="copy-btn" data-copy="${jwtToken}" style="padding: 0.25rem 0.75rem; background: rgba(102, 126, 234, 0.1); border: 1px solid var(--primary); border-radius: 6px; color: var(--primary); font-size: 0.75rem; cursor: pointer;">Copy</button>
                        <button id="openJwtIo" style="padding: 0.25rem 0.75rem; background: linear-gradient(135deg, var(--primary), var(--secondary)); border: none; border-radius: 6px; color: white; font-size: 0.75rem; cursor: pointer; font-weight: 600;">Open in JWT.io</button>
                    </div>
                </div>
                <div style="background: var(--bg-secondary); padding: 0.75rem; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.7rem; overflow-x: auto; color: var(--text-secondary); word-break: break-all;">
                    <span style="color: #fb923c;">${tokenStart}</span><span style="opacity: 0.5;">...</span><span style="color: #fb923c;">${tokenEnd}</span>
                </div>
            </div>

            <!-- JWT Header -->
            <div style="margin-bottom: 1rem;">
                <strong style="font-size: 0.875rem; display: block; margin-bottom: 0.5rem;">Header:</strong>
                <div class="response-data" style="font-size: 0.75rem;">
${JSON.stringify(jwtHeader, null, 2)}
                </div>
            </div>

            <!-- JWT Payload -->
            <div style="margin-bottom: 1rem;">
                <strong style="font-size: 0.875rem; display: block; margin-bottom: 0.5rem;">Payload:</strong>
                <div class="response-data" style="font-size: 0.75rem;">
${JSON.stringify(jwtPayload, null, 2)}
                </div>
            </div>

            <!-- HTTP Request Details -->
            <div style="margin-bottom: 1rem;">
                <strong style="font-size: 0.875rem; display: block; margin-bottom: 0.5rem;">HTTP Request:</strong>
                <div style="background: var(--bg-secondary); padding: 0.75rem; border-radius: 8px; font-family: 'Courier New', monospace; font-size: 0.75rem;">
                    <span style="color: #10b981; font-weight: bold;">POST</span> ${result.okta_endpoint || 'Okta SSF Endpoint'}<br>
                    <span style="color: #94a3b8;">Content-Type:</span> application/secevent+jwt<br>
                    <span style="color: #94a3b8;">Body:</span> [JWT Token Above]
                </div>
            </div>

            ${generateCollectedFieldsInfo(result)}
        </div>
    `;
}

// Generate collected fields info (for debugging)
function generateCollectedFieldsInfo(result) {
    if (!result.collected_fields) return '';

    const fields = result.collected_fields;
    const hasTimestamp = fields.extra_fields && fields.extra_fields.event_timestamp;

    if (!hasTimestamp && Object.keys(fields.extra_fields || {}).length === 0) return '';

    let html = `
        <div style="margin-top: 1rem; padding: 0.75rem; background: rgba(16, 185, 129, 0.05); border-left: 3px solid var(--success); border-radius: 8px;">
            <strong style="font-size: 0.875rem; display: block; margin-bottom: 0.5rem;">🔍 Field Processing:</strong>
            <div style="font-size: 0.75rem; color: var(--text-secondary);">
    `;

    if (hasTimestamp) {
        const timestamp = fields.extra_fields.event_timestamp;
        const date = new Date(timestamp * 1000);
        html += `
            <div style="margin-bottom: 0.25rem;">
                ⏰ <strong>event_timestamp</strong>: Converted to Unix timestamp
                <br>&nbsp;&nbsp;&nbsp;&nbsp;Value: ${timestamp} (${date.toLocaleString()})
            </div>
        `;
    }

    const extraFieldCount = Object.keys(fields.extra_fields || {}).length;
    if (extraFieldCount > 0) {
        html += `
            <div style="margin-top: 0.25rem;">
                ✅ Collected ${extraFieldCount} extra field(s): ${Object.keys(fields.extra_fields).join(', ')}
            </div>
        `;
    }

    html += `
            </div>
        </div>
    `;

    return html;
}

// Open JWT in jwt.io
function openInJwtIo(token) {
    // jwt.io accepts the token in the URL fragment
    const jwtIoUrl = `https://jwt.io/#debugger-io?token=${encodeURIComponent(token)}`;
    window.open(jwtIoUrl, '_blank');
}

// Show notification (simple implementation)
function showNotification(message, type) {
    const statusText = document.querySelector('.status-text');
    const statusDot = document.querySelector('.status-dot');
    const originalText = statusText.textContent;
    const originalColor = statusDot.style.background;

    statusText.textContent = message;

    if (type === 'error') {
        statusDot.style.background = '#ef4444';
    } else if (type === 'success') {
        statusDot.style.background = '#10b981';
    } else if (type === 'warning') {
        statusDot.style.background = '#f59e0b';
    }

    // Reset after 3 seconds
    setTimeout(() => {
        statusText.textContent = originalText;
        statusDot.style.background = originalColor;
    }, 3000);
}
