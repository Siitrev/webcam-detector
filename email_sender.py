import environ,os,smtplib,imghdr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header

env = environ.Env()
env.read_env(".env")

PASSWORD = os.environ.get("PASSWORD")
RECIEVER_EMAIL_ADDRESS = os.environ.get("RECIEVER_EMAIL_ADDRESS")
SENDER_EMAIL_ADDRESS = os.environ.get("SENDER_EMAIL_ADDRESS")
PORT = os.environ.get("PORT")
SMTP_SERVER_ADDRESS = os.environ.get("SMTP_SERVER_ADDRESS")

email_message="A new object has been detected now!"


def send_email(attachment):
    message = MIMEMultipart()
    message["To"] = Header(RECIEVER_EMAIL_ADDRESS)
    message["From"] = Header(SENDER_EMAIL_ADDRESS)
    message["Subject"] = Header("A new thing detected!")
    message.attach(MIMEText(email_message,"plain","utf-8"))
    
    with open(attachment, "rb") as file:
        content = file.read()
    
    message.attach(MIMEImage(content,imghdr.what(None,content)))
    
    server = smtplib.SMTP(SMTP_SERVER_ADDRESS,PORT)
    server.starttls()
    server.ehlo()
    server.login(SENDER_EMAIL_ADDRESS,PASSWORD)
    text = message.as_string()
    server.sendmail(SENDER_EMAIL_ADDRESS,RECIEVER_EMAIL_ADDRESS,text)
    server.quit()