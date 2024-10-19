import smtplib
import email.message



senha = 'mohl sauk msjw aagc'

def enviar_email():
    corpo_email = """
    <p> Ola </>

    """
    msg = email.message.Message()
    msg['Subject'] = 'Assunto'
    msg['from'] = 'tenw313@gmail.com'
    msg['To'] = 'alaiseide2006@gmail.com'
    password = senha
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # fazendo login
    s.login(msg['from'], password)
    s.sendmail(msg['from'], 
               [msg['To']], msg.as_string().encode('utf-8'))
    print('Email Enviando')


enviar_email()