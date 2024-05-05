document.addEventListener('DOMContentLoaded', function() {
    const campo_senha = document.getElementById("senha");
    const mostrar_senha = document.getElementById("mostrar_senha");
    mostrar_senha.addEventListener('change', function() {
        if (mostrar_senha.checked) {
            campo_senha.type = "text";
        } else {
            campo_senha.type = "password";
        }
    });
});