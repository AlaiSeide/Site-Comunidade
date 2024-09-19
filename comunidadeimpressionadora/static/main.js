// document.addEventListener('DOMContentLoaded', function() {
    
//     var campo_senha = document.getElementById("senha");
//     var mostrar_senha = document.getElementById("mostrar_senha");
//     console.log(campo_senha);
//     mostrar_senha.addEventListener('change', function() {
//         console.log('halo')
//         if (mostrar_senha.checked) {
//             campo_senha.type = "text";
//         } else {
//             campo_senha.type = "password";
//         }
//     });
// });


document.addEventListener('DOMContentLoaded', function() {
    // Event Listener auf das gesamte Dokument setzen
    document.addEventListener('change', function(event) {
        // Überprüfen, ob das geänderte Element die ID 'mostrar_senha' hat
        if (event.target && event.target.id === 'mostrar_senha') {
            var campo_senha = document.getElementById("senha");
            if (campo_senha) {
                if (event.target.checked) {
                    campo_senha.type = "text";
                } else {
                    campo_senha.type = "password";
                }
            }
        }
    });
});