import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

host = 'smtp.gmail.com'
port = '587'
login = 'madarah.impacta@gmail.com'
senha = 'ABCdef123-+.'


server = smtplib.SMTP(host, port)
server.ehlo()
server.starttls()
server.login(login, senha)


body = 'Essa atividade é referente a Atividade Contínua da matéria de Desenvolvimento de Aplicações na Faculdade Impacta'
subject = 'AC02 - Madarah SPTM'

email_msg = MIMEMultipart()
email_msg['From'] = login
email_msg['To'] = 'calmeida.no@gmail.com'
email_msg['Subject'] = subject
email_msg.attach(MIMEText(body, 'Plain'))


server.sendmail(
    email_msg['From'],
    email_msg['To'],
    email_msg.as_string()
)
server.quit()