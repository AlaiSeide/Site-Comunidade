# Comunidade Impressionadora
Este é um projeto de aplicação web desenvolvido com Flask. A aplicação permite aos usuários criar uma conta, fazer login, visualizar perfis, criar posts e enviar mensagens de contato.

Funcionalidades
Página Principal
A página principal exibe todos os posts em ordem decrescente de ID, ou seja, os posts mais recentes aparecem primeiro.

Contato
A página de contato contém um formulário que permite aos usuários enviar mensagens de contato. As mensagens são armazenadas no banco de dados e uma mensagem de sucesso é exibida após o envio bem-sucedido.

Usuários
A página de usuários exibe uma lista de todos os usuários registrados na aplicação. Esta página só pode ser acessada por usuários autenticados.

Login e Criação de Conta
A aplicação permite que os usuários criem uma conta e façam login. A senha do usuário é criptografada antes de ser armazenada no banco de dados. Se o login for bem-sucedido, o usuário é redirecionado para a página inicial.

Sair
Os usuários autenticados podem sair da aplicação. Após o logout, eles são redirecionados para a página inicial.

Perfil
Os usuários autenticados podem visualizar seu perfil, que exibe sua foto de perfil.

Criar Post
Os usuários autenticados podem criar um post. O post é armazenado no banco de dados e o usuário é redirecionado para a página inicial após a criação bem-sucedida do post.

Instalação e Uso
Para instalar e usar esta aplicação, você precisa ter Python e Flask instalados. Clone este repositório, instale as dependências usando pip e execute o arquivo principal.

git clone https://github.com/AlaiSeide/Site-Comunidade.git
cd comunidadeimpressionadora
pip install -r requirements.txt
python main.py

Abra seu navegador e acesse http://localhost:5000 para ver a aplicação em ação.

Contribuição
Contribuições são bem-vindas! Por favor, leia as diretrizes de contribuição antes de enviar uma pull request.

Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.
