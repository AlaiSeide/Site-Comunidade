
# Claro! O with em Python é uma maneira elegante de lidar com recursos que precisam ser abertos e fechados de forma adequada, como arquivos, conexões de banco de dados ou sockets de rede. Ele garante que os recursos sejam fechados corretamente, mesmo se ocorrerem erros durante o processamento.

# Aqui está uma explicação super simples:

# Imagine que você está lendo um livro em uma biblioteca. Você pega o livro emprestado (abre o recurso) e, quando termina de ler, você o devolve (fecha o recurso). Usando o with em Python, é como se você dissesse: "Por favor, abra este livro para mim, e quando eu terminar de ler, devolva-o automaticamente, mesmo se eu esquecer".

# Vamos ver um exemplo prático com a leitura de um arquivo:


# Sem o with
# file = open('arquivo.txt', 'r')
# conteudo = file.read()
# print(conteudo)
# file.close()  # Precisamos lembrar de fechar o arquivo

# # Com o with
# with open('arquivo.txt', 'r') as file:
#     conteudo = file.read()
#     print(conteudo)

# Aqui, o arquivo já está fechado automaticamente, não precisamos nos preocupar com isso


# import os

# temp  = os.environ['SENHA']
# print(temp)

# print(len('$2b$12$QyJPU76ZQJlAqMooSZZBv.rYzYtkxVqJDCdXS/vSjXCuuAwuysmme'))





# Armazene sempre em UTC (datetime.now(timezone.utc)).
# Converta para o fuso horário local (como Hamburgo) apenas quando for exibir ou usar o horário para interações com o usuário.


 # Calcula a data de expiração (1 hora a partir de agora)
from datetime import datetime, timedelta, timezone
data_expiracao = datetime.now(timezone.utc) + timedelta(hours=1)
print(f'Data Expiracao: {data_expiracao.strftime('%Y-%m-%d %H:%M:%S %Z')}')

print(f'UTC: {datetime.now(timezone.utc)}')

from zoneinfo import ZoneInfo
import zoneinfo
# Supondo que a hora UTC foi recuperada do banco de dados
hora_utc = datetime.now(timezone.utc)

# Convertendo para o fuso horário de Hamburgo
fuso_hamburgo = ZoneInfo("Europe/Berlin")  # Fuso horário da Alemanha
hora_local = hora_utc.astimezone(fuso_hamburgo)

print(f'Hora Local: {hora_local}')

