document.addEventListener('DOMContentLoaded', function () {
    const togglePassword = document.getElementById('togglePassword');
    const passwordField = document.getElementById('password');
    const toggleIcon = document.getElementById('toggleIcon');

    togglePassword.addEventListener('click', function () {
        // Toggle password visibility
        const isPasswordHidden = passwordField.getAttribute('type') === 'password';
        passwordField.setAttribute('type', isPasswordHidden ? 'text' : 'password');

        // Update icon
        toggleIcon.classList.toggle('fa-eye', !isPasswordHidden);
        toggleIcon.classList.toggle('fa-eye-slash', isPasswordHidden);
    });
});



<script>
    document.addEventListener('DOMContentLoaded', function () {
        flatpickr('.date-picker', {
            dateFormat: 'Y-m-d', // Format for Django DateField
        });
    });
</script>
