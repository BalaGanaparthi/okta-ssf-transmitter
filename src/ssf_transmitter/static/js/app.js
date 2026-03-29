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
        // Datetime field
        inputHtml = `
            <div class="form-group">
                <label for="${fieldId}">
                    <span class="label-text">${field.label} ${requiredLabel}</span>
                    <span class="label-hint">${field.hint} ${requiredHint}</span>
                </label>
                <div class="input-wrapper">
                    ${iconSvg}
                    <input type="datetime-local" id="${fieldId}" name="${field.name}" ${required}>
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
        for (const field of eventTypeData.field_definitions) {
            const fieldId = field.name.replace(/-/g, '_').replace(/\./g, '_');
            const element = document.getElementById(fieldId);

            if (element) {
                const value = element.value;

                // Check if required field is empty
                if (field.required && !value) {
                    showNotification(`${field.label} is required for this event type`, 'error');
                    return;
                }

                // Add to formData if has value
                if (value) {
                    formData[field.name] = value;
                }
            }
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
