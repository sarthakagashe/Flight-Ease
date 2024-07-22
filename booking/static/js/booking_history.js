// scripts.js

// You can add JavaScript functionality as needed
// Example: Cancel button click event
document.querySelectorAll('.cancel-btn').forEach(button => {
    button.addEventListener('click', () => {
        const confirmCancel = confirm('Are you sure you want to cancel this booking?');
        if (confirmCancel) {
            alert('Booking canceled');
            // Implement actual cancel functionality here
        }
    });
});
