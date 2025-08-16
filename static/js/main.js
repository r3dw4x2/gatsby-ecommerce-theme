// Main JavaScript for Data Entry System

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    initializeTooltips();
    
    // Initialize form enhancements
    initializeFormEnhancements();
    
    // Initialize table enhancements
    initializeTableEnhancements();
    
    // Initialize alert auto-dismiss
    initializeAlertAutoDismiss();
    
    // Add fade-in animation to main content
    document.querySelector('main, .container').classList.add('fade-in');
});

// Initialize Bootstrap tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Form enhancements
function initializeFormEnhancements() {
    // Character count for textarea
    const textareas = document.querySelectorAll('textarea[maxlength]');
    textareas.forEach(function(textarea) {
        addCharacterCounter(textarea);
    });
    
    // Form validation enhancement
    const forms = document.querySelectorAll('form');
    forms.forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
    
    // Auto-focus on first input
    const firstInput = document.querySelector('form input[type="text"]:first-of-type');
    if (firstInput) {
        firstInput.focus();
    }
}

// Add character counter to textareas
function addCharacterCounter(textarea) {
    const maxLength = textarea.getAttribute('maxlength');
    if (!maxLength) return;
    
    const counter = document.createElement('div');
    counter.className = 'form-text text-muted small';
    counter.innerHTML = `<span class="char-count">${textarea.value.length}</span>/${maxLength} characters`;
    
    textarea.parentNode.appendChild(counter);
    
    textarea.addEventListener('input', function() {
        const count = this.value.length;
        const span = counter.querySelector('.char-count');
        span.textContent = count;
        
        // Change color based on usage
        if (count > maxLength * 0.9) {
            span.className = 'text-warning';
        } else if (count === parseInt(maxLength)) {
            span.className = 'text-danger';
        } else {
            span.className = '';
        }
    });
}

// Table enhancements
function initializeTableEnhancements() {
    // Add hover effect to table rows
    const tableRows = document.querySelectorAll('table tbody tr');
    tableRows.forEach(function(row) {
        row.addEventListener('mouseenter', function() {
            this.style.backgroundColor = 'rgba(13, 110, 253, 0.05)';
        });
        
        row.addEventListener('mouseleave', function() {
            this.style.backgroundColor = '';
        });
    });
    
    // Add click-to-copy functionality for email and phone
    const copyableElements = document.querySelectorAll('a[href^="mailto:"], a[href^="tel:"]');
    copyableElements.forEach(function(element) {
        element.addEventListener('click', function(e) {
            e.preventDefault();
            const text = this.textContent.trim();
            copyToClipboard(text);
            showToast('Copied to clipboard: ' + text, 'success');
        });
        
        // Add tooltip
        element.setAttribute('data-bs-toggle', 'tooltip');
        element.setAttribute('title', 'Click to copy');
    });
}

// Auto-dismiss alerts
function initializeAlertAutoDismiss() {
    const alerts = document.querySelectorAll('.alert:not(.alert-danger)');
    alerts.forEach(function(alert) {
        setTimeout(function() {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000); // Auto-dismiss after 5 seconds
    });
}

// Utility function to copy text to clipboard
function copyToClipboard(text) {
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard.writeText(text);
    } else {
        // Fallback for older browsers
        const textArea = document.createElement('textarea');
        textArea.value = text;
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        try {
            document.execCommand('copy');
        } catch (err) {
            console.error('Failed to copy text: ', err);
        }
        document.body.removeChild(textArea);
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toastContainer = getOrCreateToastContainer();
    const toastId = 'toast-' + Date.now();
    const bgClass = type === 'success' ? 'bg-success' : type === 'error' ? 'bg-danger' : 'bg-info';
    
    const toastHTML = `
        <div id="${toastId}" class="toast align-items-center text-white ${bgClass} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHTML);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();
    
    // Remove from DOM after hiding
    toastElement.addEventListener('hidden.bs.toast', function() {
        this.remove();
    });
}

// Get or create toast container
function getOrCreateToastContainer() {
    let container = document.querySelector('.toast-container');
    if (!container) {
        container = document.createElement('div');
        container.className = 'toast-container position-fixed bottom-0 end-0 p-3';
        container.style.zIndex = '1050';
        document.body.appendChild(container);
    }
    return container;
}

// Confirm delete function (used in templates)
function confirmDelete(entryId, entryName) {
    document.getElementById('entryName').textContent = entryName;
    document.getElementById('deleteForm').action = '/delete/' + entryId;
    new bootstrap.Modal(document.getElementById('deleteModal')).show();
}

// API helper functions
const API = {
    // Base API configuration
    baseURL: '/api',
    
    // Generic API request handler
    async request(endpoint, options = {}) {
        const url = this.baseURL + endpoint;
        const defaultOptions = {
            headers: {
                'Content-Type': 'application/json',
            },
        };
        
        const config = { ...defaultOptions, ...options };
        
        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || 'API request failed');
            }
            
            return data;
        } catch (error) {
            console.error('API Error:', error);
            showToast('Error: ' + error.message, 'error');
            throw error;
        }
    },
    
    // Get all entries
    async getEntries() {
        return this.request('/entries');
    },
    
    // Create new entry
    async createEntry(data) {
        return this.request('/entries', {
            method: 'POST',
            body: JSON.stringify(data),
        });
    },
    
    // Update entry
    async updateEntry(id, data) {
        return this.request(`/entries/${id}`, {
            method: 'PUT',
            body: JSON.stringify(data),
        });
    },
    
    // Delete entry
    async deleteEntry(id) {
        return this.request(`/entries/${id}`, {
            method: 'DELETE',
        });
    }
};

// Export for use in other scripts
window.DataEntryAPI = API;