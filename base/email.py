from email import message
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMessage

def send_email(email,email_token):
    subject = 'Your account needs to be verified'
    email_from = settings.EMAIL_HOST_USER
    message = f'Hi, click on the link to verify your account http://127.0.0.1:8000/accounts/activate/{email_token}'

    send_mail(subject,message,email_from,[email],fail_silently=False)

def send_invoice(email,file_name):
    subject = 'Order Confirm'
    email_from = settings.EMAIL_HOST_USER
    message = 'Attached following the invoice for your purchase \n thank you for shoping with us!\n Shopall.pvt.ltd\n'
    email = EmailMessage(subject, message, email_from, [email])
    email.attach_file(str(settings.BASE_DIR)+f"/media/pdfs/{file_name}.pdf")
    email.send()
