// DOM Ready
document.addEventListener('DOMContentLoaded', function() {
    initializeTooltips();
    initializePopovers();
    setupFormValidation();
    setupCart();
    setupDateTimePickers();
});

// Initialize Bootstrap Tooltips
function initializeTooltips() {
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
}

// Initialize Bootstrap Popovers
function initializePopovers() {
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
}

// Form Validation
function setupFormValidation() {
    const forms = document.querySelectorAll('form[novalidate]');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!form.checkValidity()) {
                e.preventDefault();
                e.stopPropagation();
            }
            form.classList.add('was-validated');
        });
    });
}

// Cart Management
function setupCart() {
    const addToCartButtons = document.querySelectorAll('form[action*="add_to_cart"]');
    
    addToCartButtons.forEach(form => {
        const quantityInput = form.querySelector('input[name="quantity"]');
        
        // Increment quantity
        const incrementBtn = form.querySelector('[data-action="increment"]');
        if (incrementBtn) {
            incrementBtn.addEventListener('click', () => {
                quantityInput.value = parseInt(quantityInput.value) + 1;
            });
        }
        
        // Decrement quantity
        const decrementBtn = form.querySelector('[data-action="decrement"]');
        if (decrementBtn) {
            decrementBtn.addEventListener('click', () => {
                if (parseInt(quantityInput.value) > 1) {
                    quantityInput.value = parseInt(quantityInput.value) - 1;
                }
            });
        }
    });
}

// Date/Time Pickers - Set minimum date
function setupDateTimePickers() {
    const dateInput = document.querySelector('input[name="booking_date"]');
    if (dateInput) {
        // Set minimum date to today
        const today = new Date().toISOString().split('T')[0];
        dateInput.setAttribute('min', today);
        dateInput.addEventListener('change', function() {
            const selectedDate = new Date(this.value);
            const today = new Date();
            today.setHours(0, 0, 0, 0);
            
            if (selectedDate < today) {
                alert('Please select a future date');
                this.value = '';
            }
        });
    }
}

// Price calculation helper
function calculateTotal(price, quantity) {
    return (price * quantity).toFixed(2);
}

// Format currency
function formatCurrency(amount) {
    return '$' + parseFloat(amount).toFixed(2);
}

// Debounce function for search
function debounce(func, delay) {
    let timeoutId;
    return function(...args) {
        clearTimeout(timeoutId);
        timeoutId = setTimeout(() => func.apply(this, args), delay);
    };
}

// Search functionality
const searchInput = document.querySelector('input[name="search"]');
if (searchInput) {
    searchInput.addEventListener('input', debounce(function() {
        // Auto-submit form or trigger search
        const form = this.closest('form');
        if (form) {
            // You can add auto-submit here if desired
            // form.submit();
        }
    }, 500));
}

// Toast notification helper
function showToast(message, type = 'info') {
    const toastHTML = `
        <div class="toast align-items-center text-white bg-${type} border-0" role="alert" aria-live="assertive" aria-atomic="true">
            <div class="d-flex">
                <div class="toast-body">
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    const toastContainer = document.querySelector('.toast-container') || document.body;
    const toastElement = document.createElement('div');
    toastElement.innerHTML = toastHTML;
    toastContainer.appendChild(toastElement);
    
    const toast = new bootstrap.Toast(toastElement.querySelector('.toast'));
    toast.show();
    
    toastElement.addEventListener('hidden.bs.toast', () => {
        toastElement.remove();
    });
}

// Smooth scroll for anchor links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Logout confirmation
const logoutLink = document.querySelector('a[href*="logout"]');
if (logoutLink) {
    logoutLink.addEventListener('click', function(e) {
        // Let it proceed normally as Django handles it
    });
}

// Remove item confirmation
const removeButtons = document.querySelectorAll('form[action*="remove"] button[type="submit"]');
removeButtons.forEach(btn => {
    btn.addEventListener('click', function(e) {
        if (!confirm('Are you sure you want to remove this item?')) {
            e.preventDefault();
        }
    });
});

// Add loading state to forms
const forms = document.querySelectorAll('form[method="POST"]');
forms.forEach(form => {
    form.addEventListener('submit', function() {
        const submitButtons = this.querySelectorAll('button[type="submit"]');
        submitButtons.forEach(btn => {
            btn.disabled = true;
            btn.innerHTML = '<span class="spinner-border spinner-border-sm me-2"></span>Loading...';
        });
    });
});

// Rating stars functionality
const ratingSelects = document.querySelectorAll('select[name="rating"]');
ratingSelects.forEach(select => {
    select.addEventListener('change', function() {
        const rating = this.value;
        if (rating) {
            showToast(`You rated this ${rating} stars`, 'success');
        }
    });
});

// Filter form auto-submit
const filterSelects = document.querySelectorAll('select[onchange*="form.submit"]');
filterSelects.forEach(select => {
    select.addEventListener('change', function() {
        this.closest('form').submit();
    });
});

// Quantity input validation
const quantityInputs = document.querySelectorAll('input[name="quantity"]');
quantityInputs.forEach(input => {
    input.addEventListener('change', function() {
        const value = parseInt(this.value);
        if (value < 1) {
            this.value = 1;
        }
        if (value > 100) {
            this.value = 100;
        }
    });
});

// Number of people validation for booking
const peopleInput = document.querySelector('input[name="number_of_people"]');
if (peopleInput) {
    peopleInput.addEventListener('change', function() {
        const value = parseInt(this.value);
        if (value < 1) {
            this.value = 1;
        }
        if (value > 50) {
            this.value = 50;
            showToast('Maximum 50 people allowed. Please contact us for larger groups.', 'warning');
        }
    });
}

// Responsive table scroll
const tables = document.querySelectorAll('table');
tables.forEach(table => {
    const wrapper = document.createElement('div');
    wrapper.className = 'table-responsive';
    table.parentNode.insertBefore(wrapper, table);
    wrapper.appendChild(table);
});

// Navbar collapse on link click
const navbarCollapse = document.querySelector('.navbar-collapse');
const navbarLinks = document.querySelectorAll('.navbar-nav .nav-link');
navbarLinks.forEach(link => {
    link.addEventListener('click', function() {
        if (navbarCollapse && navbarCollapse.classList.contains('show')) {
            document.querySelector('.navbar-toggler').click();
        }
    });
});

// Set active navbar link based on current page
const currentLocation = location.pathname;
const menuItems = document.querySelectorAll('.navbar-nav .nav-link');
menuItems.forEach(item => {
    if (item.getAttribute('href') === currentLocation) {
        item.classList.add('active');
    }
});

// Export functions for use in templates if needed
window.restaurantApp = {
    showToast,
    formatCurrency,
    calculateTotal,
    debounce
};
