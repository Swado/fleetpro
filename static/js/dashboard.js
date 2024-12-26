document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    });

    // Add truck status indicators
    document.querySelectorAll('.truck-status').forEach(function(element) {
        const status = element.dataset.status;
        if (status === 'active') {
            element.classList.add('text-success');
        } else {
            element.classList.add('text-danger');
        }
    });
});
