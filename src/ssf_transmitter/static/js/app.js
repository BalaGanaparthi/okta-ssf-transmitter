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

    if (eventType && eventTypes[eventType]) {
        description.textContent = eventTypes[eventType].description;
        description.classList.add('show');

        // Clear dynamic fields
        dynamicFields.innerHTML = '';

        // Add specific fields based on event type
        if (eventType === 'USER_RISK_CHANGE') {
            dynamicFields.innerHTML = `
                <div class="form-group">
                    <label for="currentLevel">
                        <span class="label-text">Current Risk Level *</span>
                        <span class="label-hint">Current risk level (REQUIRED)</span>
                    </label>
                    <div class="select-wrapper">
                        <svg class="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M10 3.33333V16.6667M10 16.6667L15 11.6667M10 16.6667L5 11.6667" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <select id="currentLevel" name="currentLevel" required>
                            <option value="">Select current level...</option>
                            <option value="LOW">LOW</option>
                            <option value="MEDIUM">MEDIUM</option>
                            <option value="HIGH">HIGH</option>
                        </select>
                    </div>
                </div>
                <div class="form-group">
                    <label for="previousLevel">
                        <span class="label-text">Previous Risk Level *</span>
                        <span class="label-hint">Previous risk level (REQUIRED)</span>
                    </label>
                    <div class="select-wrapper">
                        <svg class="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M10 3.33333V16.6667M10 16.6667L15 11.6667M10 16.6667L5 11.6667" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <select id="previousLevel" name="previousLevel" required>
                            <option value="">Select previous level...</option>
                            <option value="LOW">LOW</option>
                            <option value="MEDIUM">MEDIUM</option>
                            <option value="HIGH">HIGH</option>
                        </select>
                    </div>
                </div>
            `;
        } else if (eventType === 'CREDENTIAL_COMPROMISE') {
            dynamicFields.innerHTML = `
                <div class="form-group">
                    <label for="credentialType">
                        <span class="label-text">Credential Type *</span>
                        <span class="label-hint">Type of credential compromised (REQUIRED)</span>
                    </label>
                    <div class="input-wrapper">
                        <svg class="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M10 3.33333V16.6667M10 16.6667L15 11.6667M10 16.6667L5 11.6667" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <input type="text" id="credentialType" name="credentialType" placeholder="e.g., password, token, api_key" required>
                    </div>
                </div>
            `;
        } else if (eventType === 'IDENTIFIER_CHANGED') {
            dynamicFields.innerHTML = `
                <div class="form-group">
                    <label for="newValue">
                        <span class="label-text">New Identifier Value (Optional)</span>
                        <span class="label-hint">New email or phone number</span>
                    </label>
                    <div class="input-wrapper">
                        <svg class="input-icon" width="20" height="20" viewBox="0 0 20 20" fill="none">
                            <path d="M2.5 6.66667L10 11.6667L17.5 6.66667M3.33333 15H16.6667C17.5871 15 18.3333 14.2538 18.3333 13.3333V6.66667C18.3333 5.74619 17.5871 5 16.6667 5H3.33333C2.41286 5 1.66667 5.74619 1.66667 6.66667V13.3333C1.66667 14.2538 2.41286 15 3.33333 15Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                        </svg>
                        <input type="text" id="newValue" name="newValue" placeholder="new-email@example.com">
                    </div>
                </div>
            `;
        }
    } else {
        description.classList.remove('show');
        dynamicFields.innerHTML = '';
    }
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
        eventType: document.getElementById('eventType').value,
        reason: document.getElementById('reason').value || null
    };

    // Add dynamic fields based on event type
    if (formData.eventType === 'USER_RISK_CHANGE') {
        formData.currentLevel = document.getElementById('currentLevel')?.value;
        formData.previousLevel = document.getElementById('previousLevel')?.value;
    } else if (formData.eventType === 'CREDENTIAL_COMPROMISE') {
        formData.credentialType = document.getElementById('credentialType')?.value;
    } else if (formData.eventType === 'IDENTIFIER_CHANGED') {
        formData.newValue = document.getElementById('newValue')?.value || null;
    }

    // Validate
    if (!formData.subject || !formData.eventType) {
        showNotification('Please fill in all required fields', 'error');
        return;
    }

    // Validate event-specific required fields
    if (formData.eventType === 'USER_RISK_CHANGE') {
        if (!formData.currentLevel || !formData.previousLevel) {
            showNotification('Current and Previous Risk Level are required for this event type', 'error');
            return;
        }
    } else if (formData.eventType === 'CREDENTIAL_COMPROMISE') {
        if (!formData.credentialType) {
            showNotification('Credential Type is required for this event type', 'error');
            return;
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
                ${result.data ? `<div class="response-data">${JSON.stringify(result.data, null, 2)}</div>` : ''}
            </div>
        `;
    } else {
        html = `
            <div class="response-error">
                <span class="response-label">❌ Error</span>
                ${result.status ? `<p><strong>Status:</strong> ${result.status}</p>` : ''}
                ${result.error ? `<p><strong>Error:</strong> ${typeof result.error === 'object' ? JSON.stringify(result.error) : result.error}</p>` : ''}
                ${result.details ? `<p><strong>Details:</strong> ${result.details}</p>` : ''}
                ${result.error && typeof result.error === 'object' ? `<div class="response-data">${JSON.stringify(result.error, null, 2)}</div>` : ''}
            </div>
        `;
    }

    responseContent.innerHTML = html;
    responseCard.style.display = 'block';

    // Scroll to response
    responseCard.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
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
