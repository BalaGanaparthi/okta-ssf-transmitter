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

// Populate event type dropdown
function populateEventTypes() {
    const select = document.getElementById('eventType');
    const placeholder = select.querySelector('option[value=""]');

    Object.keys(eventTypes).forEach(key => {
        const option = document.createElement('option');
        option.value = key;
        option.textContent = eventTypes[key].label;
        select.appendChild(option);
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

    if (eventType && eventTypes[eventType]) {
        description.textContent = eventTypes[eventType].description;
        description.classList.add('show');
    } else {
        description.classList.remove('show');
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

    // Validate
    if (!formData.subject || !formData.eventType) {
        showNotification('Please fill in all required fields', 'error');
        return;
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
