from django.conf import settings
from django.core.mail import send_mail

class EmailSender:

    def send_email(self, destinatarios, asunto, cuerpo):
        #El mensaje será enviado desde la dirección email definida en settings.py
        remitente = settings.EMAIL_HOST_USER    
        mensajes_enviados = send_mail(
        asunto,
        cuerpo,  
        remitente,
        destinatarios,
        fail_silently=False)
        return mensajes_enviados