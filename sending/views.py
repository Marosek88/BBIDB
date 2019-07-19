from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import get_template
from BBI_DB import settings

from bbidb_app.models import Category, Company, Contact, Project, ProjectContact, ProjectContactWorks, Change_Log
from django.contrib.auth.models import User

@login_required
def sending_send_invite(request, project_contact_id):
    user = request.user
    project_contact = ProjectContact.objects.get(id=project_contact_id)
    project = project_contact.project
    works = project_contact.works

    to_email = [user.email]  # FOR TESTING, CHANGE AFTER TO project_contact.contact.email
    cc = []  # ADD CC PEOPLE FOR DEPLOYMENT
    from_email = settings.EMAIL_HOST_USER
    reply_to = [user.email]
    subject = project.name + ' - Tender Invitation'
    body = ''
    context = {
        'user': user,
        'project_contact': project_contact,
        'project': project,
        'works': works
    }

    # generate html message, attach it to the composed message and send it
    html_template = get_template('sending/sending_invite.html').render(context)
    message = EmailMultiAlternatives(subject="[BBIDB] " + subject, body=body, from_email=from_email, to=to_email, reply_to=reply_to,
                                     cc=cc)
    message.attach_alternative(html_template, "text/html")
    message.send()

    # change email_sent status to project_contact
    project_contact.email_sent_date = now()
    # mark the contact as used now
    project_contact.contact.date_used = now()
    project_contact.save()



@login_required
def sending_invite(request, project_contact_id):

    # use the above function to send an invite
    sending_send_invite(request, project_contact_id)

    # communicate success on website
    messages.success(request, 'Email has been sent successfully')

    return redirect('bbidb:project_contact_message_manage', project_contact_id)


@login_required
def sending_bulk_invite(request, project_id):
    #receiving info from POST form
    req = request.POST
    project_contact_list = req.getlist('project_contact')
    project = Project.objects.get(id=req['project'])

    # send the message one by one using the above function
    invites_sent = ''
    for project_contact_id in project_contact_list:
        sending_send_invite(request, int(project_contact_id))
        project_contact = ProjectContact.objects.get(id=int(project_contact_id))
        invites_sent += f"{project_contact.contact.name} {project_contact.contact.surname}, "

    #confirm that all went well
    messages.success(request, 'All messages have been sent')
    Change_Log.objects.create(category="Invite", user=request.user,
                              log=f"Sent Invites in {project.name} to: \n{invites_sent}",
                              log_date=now())
    return redirect('bbidb:project_contacts', project_id)
