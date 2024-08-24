
import smtplib
from email.mime.text import MIMEText

subject = "Chat Bot Appointment"
body = "Your appointment has been approved your date and time is" #pull out kaman sa data ka e butang guro di gha
sender = "michaelleguira@gmail.com" #email nanda ja tudluan talang mag setup sunod
recipients = ["michaelleguira@gmail.com"] #pull out mo sa database ang email account sang user sa tblpatient
password = "gotu yidg qrzy waml"


def send_email (subject, body, sender, recipients, password):
     msg = MIMEText(body)
     msg['Subject'] = subject
     msg['From'] = sender
     msg['To'] = ', '.join(recipients)
     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp_server:
          smtp_server.login(sender, password)
          smtp_server.sendmail(sender, recipients, msg.as_string())
     print ("Message sent!")


#for testing only
#send_email(subject, body, sender, recipients, password)
     
