from django.conf import settings
from django.core.mail import EmailMessage, EmailMultiAlternatives, send_mail
from django.shortcuts import render
from django.template.loader import render_to_string
from django.views import View

from .forms import EmailForm


class EmailAttach(View):
    form_class = EmailForm
    template_name = 'emailattachment.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'email_form': form})

    # send email without attachment using smtp.gmail
    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            subject = 'Email with Attachment'
            message = form.cleaned_data['message']
            email = form.cleaned_data['email']
            attachment_path = request.FILES.getlist('attach')
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email, ]
            try:
                # ### send email with attachment
                mail = EmailMessage(subject, message, email_from, recipient_list)
                for file in attachment_path:
                    mail.attach(file.name, file.read(), file.content_type)
                mail.send()

                # ### sending email with custom template
                # html_content = render_to_string('custom_email_template.html',
                #                                 {'message': message, 'subject': subject})
                # send_mail(subject, message, email_from, recipient_list, fail_silently=False,html_message= html_content)


                return render(request, self.template_name, {'email_form': form, 'error_message': 'Sent email to %s'%email})
            except:
                return render(request, self.template_name,
                              {'email_form': form, 'error_message': 'Either the attachment is too big or corrupt'})

        return render(request, self.template_name,
                      {'email_form': form, 'error_message': 'Unable to send email. Please try again later'})
