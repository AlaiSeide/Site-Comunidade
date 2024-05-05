document.addEventListener("DOMContentLoaded", function() {
    var campo = document.getElementById("senha");
    var mensagemDiv = document.getElementById("mensagem_caps_lock");

    campo.addEventListener("keyup", function(event) {
        if (event.getModifierState("CapsLock")) {
            mensagemDiv.innerText = "Teclado de Maiúsculas ativado!";
            mensagemDiv.style.color = "red";    
        } else {
            mensagemDiv.innerText = "";
           
        }
    });
});
