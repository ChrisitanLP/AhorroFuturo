document.addEventListener('DOMContentLoaded', function() {
    const asterisks = document.querySelectorAll('.asteriskField');
    asterisks.forEach(function(asterisk) {
        asterisk.style.display = 'none';
    });
    
    // Quitar cualquier clase que pueda interferir con el diseño
    const inputs = document.querySelectorAll('.form-control');
    inputs.forEach(function(input) {
        input.classList.remove('is-invalid');
    });
});