# uma funcao que vai fazer todas as validacoes da imagem e salvar-la
def salvar_imagem(imagem):
    # adicionar um codigo aleatorio no nome da imagem
    codigo = secrets.token_hex(8)
    # separar o nome do arquivo com a extensao
    nome, extensao = os.path.splitext(imagem.filename)
    # juntar nome, codigo e a extensao
    nome_arquivo = nome + codigo + extensao
    # salvar a imagem na pasta fotos_perfil
    #  o app.root_path seria o caminho do novo app que é comunidadeimpressionadora
    caminho_completo = os.path.join(app.root_path, 'static/fotos_perfil', nome_arquivo)
    # reduzir o tamanho da imagem
    # 200x200 px
    tamanho = (200, 200)
    imagem_reduzida = Image.open(imagem)
    imagem_reduzida.thumbnail(tamanho)
    # salvar a imagem na pasta fotos_perfil
    imagem_reduzida.save(caminho_completo)
    # mudar o campo foto_perfil do usuario para o novo nome
    return nome_arquivo

# uma funcao para atualizar os cursos 
def atualizar_cursos(formulario):
    lista_cursos = []
    # percorrer todos os campos de cursos do formulario
    for campo in formulario:
        # verifica se o campo do formulario comeca com curso_
        if 'curso_' in campo.name:
            # verificar se o campo for marcado
            if campo.data:
                # adicionar o texto do campo.label  (Excel Impressionador) na lista de cursos
                lista_cursos.append(campo.label.text)
    # Então, se lista_cursos fosse ['Curso1', 'Curso2', 'Curso3'], a linha de código retornaria a string 'Curso1;Curso2;Curso3'. Espero que isso esclareça! Se você tiver mais perguntas, fique à vontade para
    return ';'.join(lista_cursos)


