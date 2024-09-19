document.addEventListener("DOMContentLoaded", function() {
    // Delegação de evento para 'keyup' no documento inteiro
    document.addEventListener("keyup", function(event) {
        // Verifica se o elemento que disparou o evento tem o ID 'senha'
        if (event.target && event.target.id === "senha") {
            var mensagemDiv = document.getElementById("mensagem_caps_lock");
            if (event.getModifierState("CapsLock")) {
                mensagemDiv.innerText = "Teclado de Maiúsculas ativado!";
                mensagemDiv.style.color = "red";    
            } else {
                mensagemDiv.innerText = "";
            }
        }
    });
});