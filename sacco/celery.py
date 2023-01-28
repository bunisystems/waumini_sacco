from __future__ import absolute_import, unicode_literals
from celery import Celery, shared_task
from django.conf import settings
from django.core.mail import send_mail
from django.core.mail import EmailMultiAlternatives

app = Celery('sacco')
app.config_from_object('django.conf:settings', namespace='CELERY')


app = Celery('core')
app.config_from_object('django.conf:settings', namespace='CELERY')

@app.task
def send_account_creation_email(to_email, f_name, l_name, username, url):
    to = to_email
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = '[Waumini Sacco] Account Creation'
    text_content = subject
    html_content = '<p>Dear ' + f_name + ' ' + l_name + ', Your account has been created. </p><p>Please following the link( https://' + url + ' ) to reset your password<ul>' + 'Username:' + str(username) + '</ul><ul>' + 'E-mail: ' + str(to_email) + '</ul></p>'
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
