import smtplib
from email.message import EmailMessage

msg = EmailMessage()
msg.set_content('')

msg['Subject'] = ''
msg['From'] = 'test@gmail.com'
msg['To'] = ''

s = smtplib.SMTP('smtp-relay.sendinblue.com:587')
s.login("username", "password")
s.send_message(msg)
s.quit()

