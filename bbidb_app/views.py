import csv, io
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.views.generic.edit import CreateView, UpdateView
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.db.utils import DataError, IntegrityError

from bbidb_app.models import Category, Company, Contact, Project, ProjectContact, ProjectContactWorks, Change_Log
from django.contrib.auth.models import User



@method_decorator(login_required, name="dispatch")
class CompanyCreate(CreateView):
    template_name = 'company_form.html'
    model = Company
    fields = ['name', 'head_address', 'head_phone', 'head_email', 'website', 'company_logo', 'remarks']


@method_decorator(login_required, name="dispatch")
class CompanyUpdate(UpdateView):
    template_name = 'company_form.html'
    model = Company
    fields = ['name', 'head_address', 'head_phone', 'head_email', 'website', 'company_logo', 'remarks']


@method_decorator(login_required, name="dispatch")
class ContactCreate(CreateView):
    template_name = 'contact_form.html'
    model = Contact
    fields = ['company', 'category', 'name', 'surname', 'role', 'address', 'phone', 'mobile', 'email', 'remarks']


@method_decorator(login_required, name="dispatch")
class ContactUpdate(UpdateView):
    template_name = 'contact_form.html'
    model = Contact
    fields = ['company', 'category', 'name', 'surname', 'role', 'address', 'phone', 'mobile', 'email', 'remarks']


@method_decorator(login_required, name="dispatch")
class ProjectCreate(CreateView):
    template_name = 'project_form.html'
    model = Project
    fields = ['name', 'status', 'description', 'boq', 'tender_submission', 'contract_start', 'remarks', 'email_cc',
              'email_quotation_deadline', 'email_greeting', 'email_invitation1', 'email_invitation2',
              'email_description1', 'email_attachment2', 'email_attachment_full', 'email_note1', 'email_note2',
              'email_note3', 'email_general_notes']


@method_decorator(login_required, name="dispatch")
class ProjectUpdate(UpdateView):
    template_name = 'project_form.html'
    model = Project
    fields = ['name', 'status', 'description', 'boq', 'tender_submission', 'contract_start', 'remarks', 'email_cc',
              'email_quotation_deadline', 'email_greeting', 'email_invitation1', 'email_invitation2',
              'email_description1', 'email_attachment2', 'email_attachment_full', 'email_note1', 'email_note2',
              'email_note3', 'email_general_notes']


@method_decorator(login_required, name="dispatch")
class ProjectContactCreate(CreateView):
    template_name = 'project_contact_form.html'
    model = ProjectContact
    fields = ['project', 'contact', 'works', 'attachment', 'remarks', 'assigned_to', 'email_sent_date',
              'will_price_date', 'not_interested_date',
              'requires_clarification_date', 'quotation_received', 'email_personal_message']


@method_decorator(login_required, name="dispatch")
class ProjectContactUpdate(UpdateView):
    template_name = 'project_contact_form.html'
    model = ProjectContact
    fields = ['project', 'contact', 'works', 'attachment', 'remarks', 'assigned_to', 'email_sent_date',
              'will_price_date', 'not_interested_date',
              'requires_clarification_date', 'quotation_received', 'email_personal_message']


@method_decorator(login_required, name="dispatch")
class ProjectContactWorksCreate(CreateView):
    template_name = 'project_contact_works_form.html'
    model = ProjectContactWorks
    fields = ['project', 'name', 'email_message', 'email_attachment_message', 'email_category_attachment']


@method_decorator(login_required, name="dispatch")
class ProjectContactWorksUpdate(UpdateView):
    template_name = 'project_contact_works_form.html'
    model = ProjectContactWorks
    fields = ['project', 'name', 'email_message', 'email_attachment_message', 'email_category_attachment']


@login_required
def index(request):
    if request.POST:
        req = request.POST
        if req != "-1":
            picked_user = User.objects.get(id=int(req['user_id']))
            my_project_contacts_to_send = ProjectContact.objects.filter(assigned_to=picked_user,
                                                                        email_sent_date=None, archivised=False)
            my_project_contacts_clarification = ProjectContact.objects.filter(assigned_to=picked_user,
                                                                              archivised=False).exclude(
                requires_clarification_date=None)
        else:
            messages.warning(request, 'Choose a user to change the tables')
            return redirect('bbidb:index')

    else:
        my_project_contacts_to_send = ProjectContact.objects.filter(assigned_to=request.user,
                                                                    email_sent_date=None, archivised=False)
        my_project_contacts_clarification = ProjectContact.objects.filter(assigned_to=request.user,
                                                                          archivised=False).exclude(
            requires_clarification_date=None)

    context = {
        'active_users': User.objects.filter(is_active=True),
        'companies': Company.objects.filter(archivised=False),
        'contacts': Contact.objects.filter(archivised=False),
        'categories': Category.objects.filter(archivised=False),
        'projects': Project.objects.filter(archivised=False),
        'open_projects': Project.objects.filter(archivised=False, status=True).order_by('name'),
        'my_project_contacts_to_send': my_project_contacts_to_send,
        'my_project_contacts_clarification': my_project_contacts_clarification
    }

    if request.POST:
        the_user = User.objects.get(id=int(request.POST['user_id']))
        context['the_user'] = the_user

    return render(request, 'index.html', context)


@login_required
def import_multiple(request):
    return render(request, 'import_multiple.html')


@login_required
def import_action(request):
    req = request.POST
    action = req['action_no']

    if action == "-1":
        messages.warning(request, 'Please choose what to import')
        return redirect('bbidb:import_multiple')

    if action == 'categories':
        # load file
        csv_file = request.FILES['file']

        # make sure it's CSV
        if not csv_file.name.endswith('.csv'):
            messages.warning(request, 'Only CSV files can be imported')
            return redirect('bbidb:import_multiple')

        # set decode chars
        data_set = csv_file.read().decode('UTF-8')

        # set stream
        io_string = io.StringIO(data_set)

        # skip first CSV file line (header)
        next(io_string)

        added = 0
        cats = ''
        for column in csv.reader(io_string, delimiter=',', quotechar="|"):
            try:
                Category.objects.create(name=column[0])
                added += 1
                cats += f'{column[0]}, '
            except:
                messages.warning(request, f"{column[0]} can't be loaded - it's duplicated or name longer than 100 char")

        Change_Log.objects.create(category="Category", user=request.user,
                                  log=f"Imported Multiple {added} Categories \n{cats}", log_date=now())
        messages.success(request, f'Import of {added} Categories Successful')
        return redirect('bbidb:import_multiple')

    if action == 'companies':
        # load file
        csv_file = request.FILES['file']

        # make sure it's CSV
        if not csv_file.name.endswith('.csv'):
            messages.warning(request, 'Only CSV files can be imported')
            return redirect('bbidb:import_multiple')

        try:
            # set decode chars
            data_set = csv_file.read().decode('UTF-8')

            # set stream
            io_string = io.StringIO(data_set)

            # skip first CSV file line (header)
            next(io_string)

            added = 0
            comp = ''
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                # throwaway variable (saves without save() )
                try:
                    _, created = Company.objects.update_or_create(
                        name=column[0],
                        head_address=column[1],
                        head_phone=column[2],
                        head_email=column[3],
                        website=column[4],
                        remarks=column[5],
                        added_by=str(request.user.first_name) + ' ' + str(request.user.last_name)
                    )

                    added += 1
                    comp += f'{column[0]}, '
                except DataError:
                    messages.warning(request, f"{column[0]} cant't be loaded - name is over 100 char long")
                except IntegrityError as e:
                    messages.warning(request, f"Integrity Error: {e}")

            messages.success(request, 'Companies Import Successful')
            Change_Log.objects.create(category="Company", user=request.user,
                                      log=f"Imported Multiple {added} Companies: \n{comp}", log_date=now())
        except UnicodeDecodeError as e:
            messages.warning(request, f"File Loading Error: {e}")

        return redirect('bbidb:import_multiple')

    if action == 'contacts':
        # load file
        csv_file = request.FILES['file']

        # make sure it's CSV
        if not csv_file.name.endswith('.csv'):
            messages.warning(request, 'Only CSV files can be imported')
            return redirect('bbidb:import_multiple')

        try:
            # set decode chars
            data_set = csv_file.read().decode('UTF-8')

            # set stream
            io_string = io.StringIO(data_set)

            # skip first CSV file line (header)
            next(io_string)

            # add contacts
            added = 0
            conts = ''
            for column in csv.reader(io_string, delimiter=',', quotechar="|"):
                try:
                    created = Contact.objects.create(
                        company=Company.objects.get(name=column[0]),
                        name=column[2],
                        surname=column[3],
                        role=column[4],
                        address=column[5],
                        phone=column[6],
                        mobile=column[7],
                        email=column[8],
                        remarks=column[9],
                        added_by=str(request.user.first_name) + ' ' + str(request.user.last_name)
                    )
                    created.save()

                except ObjectDoesNotExist:
                    messages.warning(request,
                                     f"{column[2]} {column[3]} couldn't be loaded - ({column[0]} doesn't exist or is misspelled)")
                    continue
                except MultipleObjectsReturned:
                    messages.warning(request,
                                     f"{column[2]} {column[3]} couldn't be loaded - ({column[0]} seems to be duplicated)")
                    continue
                except DataError:
                    messages.warning(request,
                                     f"{column[2]} {column[3]} couldn't be loaded - one of the fields is over 100 char long")
                    continue

                if created:
                    # add multiple categories
                    categories = column[1].split(";")
                    for category in categories:
                        try:
                            created.category.add(Category.objects.get(name=category))
                        except ObjectDoesNotExist:
                            messages.warning(request, f"{category} was not added to {column[2]} {column[3]}")
                    added += 1
                    conts += f'{column[2]} {column[3]},'

            messages.success(request, f'{added} Contacts Import Successful')
            Change_Log.objects.create(category="Contact", user=request.user,
                                      log=f"Imported Multiple {added} Contacts: \n{conts}", log_date=now())
        except UnicodeDecodeError as e:
            messages.warning(request, f"File Loading Error: {e}")

        return redirect('bbidb:import_multiple')

    else:
        messages.warning(request, 'Something Went Wrong')
        return redirect('bbidb:import_multiple')


@login_required
def companies(request):
    context = {
        'companies': Company.objects.filter(archivised=False).order_by('name'),
    }
    return render(request, 'companies.html', context)


@login_required
def company_details(request, company_id):
    company = Company.objects.get(id=int(company_id))
    contacts = company.contact_set.filter(archivised=False)
    project_contacts = {}
    for contact in contacts:
        project_contacts[contact] = []
        for project_contact in contact.projectcontact_set.filter(archivised=False):
            project_contacts[contact].append(project_contact)

    context = {
        'company': company,
        'contacts': contacts,
        'project_contacts': project_contacts,
    }
    return render(request, 'company_details.html', context)


@login_required
def company_action(request):
    req = request.POST
    action = str(req['action_no'])
    company_list = req.getlist('company')
    company_list_len = len(company_list)

    if action == "-1":
        messages.warning(request, 'Choose an Action to perform')
        return redirect('bbidb:companies')

    elif action == "archive":
        for company in company_list:
            comp = Company.objects.get(id=int(company))

            comp.archivised = True
            comp.archivised_date = now()
            comp.save()

        messages.success(request, f'{company_list_len} item(s) archivised!')
        Change_Log.objects.create(category="Company", user=request.user,
                                  log=f"Archivised Company: {comp.name}", log_date=now())
        return redirect('bbidb:companies')

    else:
        messages.success(request, "Something went wrong")
        return redirect('bbidb:companies')


@login_required
def company_updated(request, company_id):
    company = Company.objects.get(id=company_id)
    company.date_updated = now()
    company.save()

    messages.success(request, f'{company.name} has been successfully added / updated')
    Change_Log.objects.create(category="Company", user=request.user,
                              log=f"Updated Company {company.name}", log_date=now())
    return redirect('bbidb:companies')


# @login_required
# def contact_details(request, contact_id):
#     contact = get_object_or_404(Contact, pk=contact_id)
#     context = {
#         'contact': contact,
#     }
#     return render(request, 'contact_details.html', context)

@login_required
def contacts(request):
    context = {
        'contacts': Contact.objects.filter(archivised=False).order_by('name'),
        'projects': Project.objects.filter(archivised=False).order_by('name'),
    }
    return render(request, 'contacts.html', context)


@login_required
def contact_details(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    context = {
        'contact': contact,
        'project_contacts': contact.projectcontact_set.all().order_by('archivised'),
    }
    return render(request, 'contact_details.html', context)


@login_required
def contact_action(request):
    req = request.POST
    action = str(req['action_no'])
    contact_list = req.getlist('contact')
    contact_list_len = len(contact_list)
    context = {
        'contacts': Contact.objects.filter(archivised=False),
        'projects': Project.objects.filter(archivised=False).order_by('name'),
        'contact': contact_list,
        'contact_len': contact_list_len,
    }

    if action == "-1":
        messages.warning(request, 'Choose an Action to perform')
        return redirect('bbidb:contacts')

    elif action == "add_to_project":

        project_number = int(req['project_no'])
        context['project'] = project_number

        added = 0
        if project_number == -1 and contact_list_len == 0:
            messages.warning(request, 'Select Project and Contacts to add mate')
            return redirect('bbidb:contacts')
        elif project_number == -1:
            messages.warning(request, 'Select Project to add the Contacts bud')
            return redirect('bbidb:contacts')
        elif contact_list_len == 0:
            messages.warning(request, 'Select Contacts to add laddy')
            return redirect('bbidb:contacts')
        else:
            project = Project.objects.get(id=project_number)
            project_contacts = project.projectcontact_set.filter(archivised=False)

            conts = ''
            for contact in contact_list:
                exists = 0
                for project_contact in project_contacts:
                    if project_contact.contact.id == int(contact):
                        exists = 1
                        break

                if exists == 1:
                    cont = Contact.objects.get(id=int(contact))
                    messages.warning(request, str(cont.name) + ' ' + str(cont.surname) + ' is already in ' + str(
                        project.name))
                else:
                    # if contact doesn't exist in project - add new one

                    # create a new temporary contact and update it's 'date_used' field
                    temp_contact = Contact.objects.get(id=int(contact))
                    temp_contact.date_used = now()
                    temp_contact.save()

                    # create a list of selected categories for that contact
                    chosen_categories = req.getlist('chosen_category' + contact)

                    # create a name for the works basing on selected categories
                    temp_work = ""
                    for chosen_category in chosen_categories:
                        temp_work += ' / ' + chosen_category
                    temp_work = temp_work[2:]

                    # check if works name exists
                    project_works = project.projectcontactworks_set.filter(archivised=False, project=project)
                    work_exists = 0
                    for project_work in project_works:

                        if project_work.category == temp_work:
                            work_exists = 1

                            temp_work_to_assign = project_work
                            temp_project_contact = ProjectContact.objects.create(
                                project=project,
                                contact=Contact.objects.get(id=int(contact)), works=temp_work_to_assign)
                            temp_project_contact.save()
                            break

                    if work_exists == 0:
                        temp_work_to_assign = ProjectContactWorks.objects.create(category=temp_work, name=temp_work,
                                                                                 project=project)
                        temp_project_contact = ProjectContact.objects.create(
                            project=project,
                            contact=Contact.objects.get(id=int(contact)), works=temp_work_to_assign)
                        temp_project_contact.save()

                    added += 1
                    if temp_project_contact.contact.name:
                        conts += f'{temp_project_contact.contact.name} {temp_project_contact.contact.surname}, '
                    else:
                        conts += f'Info for {temp_project_contact.contact.company.name}, '

            Change_Log.objects.create(category="ProCon", user=request.user,
                                      log=f"Added {added} Contacts to {project.name}: \n{conts}", log_date=now())
            messages.success(request, str(added) + ' Contacts added to ' + project.name)

        return redirect('bbidb:contacts')

    elif action == "archive":
        for contact in contact_list:
            cont = Contact.objects.get(id=int(contact))
            cont.archivised = True
            cont.archivised_date = now()
            cont.save()

        messages.success(request, f'{contact_list_len} item(s) archivised!')
        Change_Log.objects.create(category="Contact", user=request.user,
                                  log=f"Archivised Contact {cont.name} {cont.surname}", log_date=now())
        return redirect('bbidb:contacts')

    else:
        messages.warning(request, 'Something went wrong')
        return redirect('bbidb:contacts')


@login_required
def contact_updated(request, contact_id):
    contact = Contact.objects.get(id=contact_id)
    contact.date_updated = now()
    contact.save()
    if contact.name:
        messages.success(request, f'{contact.name} {contact.surname} has been successfully added / updated')
        Change_Log.objects.create(category="Contact", user=request.user,
                                  log=f"Updated Contact {contact.name} {contact.surname}", log_date=now())
    else:
        messages.success(request, f'Info for {contact.company.name} has been successfully added / updated')
        Change_Log.objects.create(category="Contact", user=request.user,
                                  log=f"Updated Contact Info for {contact.company.name}", log_date=now())

    return redirect('bbidb:contacts')


# @login_required
# def contact_archive(request, contact_id):
#     contact = Contact.objects.get(id=contact_id)
#     contact.archivised = True
#     contact.save()
#     return redirect('bbidb:contacts')


@login_required
def projects(request):
    context = {
        'projects': Project.objects.filter(archivised=False).order_by('name'),
    }
    return render(request, 'projects.html', context)


@login_required
def project_action(request):
    req = request.POST
    action = str(req['action_no'])
    project_list = req.getlist('project')
    project_list_len = len(project_list)

    if action == "-1":
        messages.warning(request, 'Choose an Action to perform')
        return redirect('bbidb:projects')

    elif action == "archive":
        for project in project_list:
            proj = Project.objects.get(id=int(project))
            proj.archivised = True
            proj.archivised_date = now()
            proj.save()

        messages.success(request, f'{project_list_len} item(s) archivised!')
        Change_Log.objects.create(category="Project", user=request.user,
                                  log=f"Archivised Project {proj.name}", log_date=now())
        return redirect('bbidb:projects')

    else:
        messages.warning(request, "Something went wrong")
        return redirect('bbidb:projects')


@login_required
def project_updated(request, project_id):
    project = Project.objects.get(id=project_id)
    project.date_updated = now()
    project.save()

    messages.success(request, f'{project.name} has been successfully added / updated')
    Change_Log.objects.create(category="Project", user=request.user,
                              log=f"Updated Project {project.name}", log_date=now())
    return redirect('bbidb:projects')


# def project_archive(project_id):
#     project = Project.objects.get(id=project_id)
#     project.archivised = True
#     project.save()


# @login_required
# def project_archive(request, project_id):
#     project = Project.objects.get(id=project_id)
#     project.archivised = True
#     project.save()
#     return redirect('bbidb:projects')


@login_required
def project_contacts(request, project_id):
    project = Project.objects.get(id=project_id)
    project_contacts = project.projectcontact_set.filter(archivised=False).order_by('works')
    outstanding_invites = project_contacts.filter(email_sent_date=None)
    emails_sent = project_contacts.exclude(email_sent_date=None).count() / project_contacts.count() * 100
    outstanding_clarifications = project_contacts.exclude(requires_clarification_date=None)
    will_price = project_contacts.exclude(will_price_date=None).count() / project_contacts.count() * 100
    wont_price = project_contacts.exclude(not_interested_date=None).count() / project_contacts.count() * 100
    not_sure = project_contacts.filter(will_price_date=None, not_interested_date=None).count() / project_contacts.count() * 100
    quotation_received = project_contacts.exclude(quotation_received=None).count() / project_contacts.count() * 100


    context = {
        'outstanding_invites': outstanding_invites,
        'emails_sent': emails_sent,
        'emails_to_send': 100-emails_sent,
        'my_outstanding_invites': outstanding_invites.filter(assigned_to=request.user),
        'outstanding_clarifications': outstanding_clarifications,
        'my_outstanding_clarifications': outstanding_clarifications.filter(assigned_to=request.user),
        'will_price': will_price,
        'wont_price': wont_price,
        'not_sure': not_sure,
        'quotation_received': quotation_received,
        'project': project,
        'project_contacts': project_contacts,
        'works': ProjectContactWorks.objects.filter(archivised=False, project=project).order_by('name'),
        'users': User.objects.filter(is_active=True),
    }
    return render(request, 'project_contacts.html', context)


@login_required
def project_contact_action(request):
    req = request.POST
    action = str(req['action_no'])
    project_contact_list = req.getlist('project_contact')
    project_contact_list_len = len(project_contact_list)
    project_id = int(req['project_id'])
    project = Project.objects.get(id=project_id)

    if action == "-1":
        messages.warning(request, 'Choose an Action to perform')
        return redirect('bbidb:project_contacts', project_id)

    elif action == "add_to_works":
        work = ProjectContactWorks.objects.get(id=int(req['works_no']))
        for project_contact in project_contact_list:
            project_cont = ProjectContact.objects.get(id=int(project_contact))
            project_cont.works = work
            project_cont.save()

        messages.success(request, f'{project_contact_list_len} item(s) added to {work.name}!')
        Change_Log.objects.create(category="ProCon", user=request.user,
                                  log=f"Added Project Contact in {project.name} to {work.name}: {project_cont.contact.name} {project_cont.contact.surname}",
                                  log_date=now())
        return redirect('bbidb:project_contacts', project_id)

    elif action == "assign_user":
        user = User.objects.get(id=int(req['user_id']))
        for project_contact in project_contact_list:
            project_cont = ProjectContact.objects.get(id=int(project_contact))
            project_cont.assigned_to = user
            project_cont.save()

        messages.success(request, f'{project_contact_list_len} item(s) assigned to {user.first_name} {user.last_name}!')
        Change_Log.objects.create(category="ProCon", user=request.user,
                                  log=f"Assigned Project Contact in {project.name} to {user.first_name} {user.last_name}: {project_cont.contact.name} {project_cont.contact.surname}",
                                  log_date=now())
        return redirect('bbidb:project_contacts', project_id)

    elif action == "change_status":
        invite_sent = req["invite_sent"]
        clarification_req = req["clarification_req"]
        pricing = req["pricing"]
        quotation_received = req["quotation_received"]
        for project_contact in project_contact_list:
            project_cont = ProjectContact.objects.get(id=int(project_contact))
            status_change = ''
            if invite_sent != "-1":
                if bool(invite_sent):
                    project_cont.email_sent_date = now()
                    project_cont.contact.date_used = now()
                    status_change += f'Invite sent: Yes, '
                else:
                    project_cont.email_sent_date = None
                    status_change += f'Invite sent: No, '
            if clarification_req != "-1":
                if bool(clarification_req):
                    project_cont.requires_clarification_date = now()
                    status_change += f'Clarification required: Yes, '
                else:
                    project_cont.requires_clarification_date = None
                    status_change += f'Clarification required: No, '
            if pricing != "-1":
                if pricing == "yes":
                    project_cont.will_price_date = now()
                    project_cont.not_interested_date = None
                    status_change += f'Will price: Yes, '
                elif pricing == "no":
                    project_cont.will_price_date = None
                    project_cont.not_interested_date = now()
                    status_change += f'Will price: No, '
                else:
                    project_cont.will_price_date = None
                    project_cont.not_interested_date = None
                    status_change += f'Will price: Not Confirmed, '
            if quotation_received != "-1":
                if bool(quotation_received):
                    project_cont.quotation_received = now()
                    status_change += f'Quotation received: Yes, '
                else:
                    project_cont.quotation_received = None
                    status_change += f'Quotation received: No, '
            project_cont.save()

        messages.success(request, f'{project_contact_list_len} item(s) have been updated!')
        Change_Log.objects.create(category="ProCon", user=request.user,
                                  log=f"Status Updted Project Contact in {project_cont.project.name}: {project_cont.contact.name} {project_cont.contact.surname}: {status_change}",
                                  log_date=now())
        return redirect('bbidb:project_contacts', project_id)


    elif action == "send_bulk_invites":

        context = {
            'project': Project.objects.get(id=project_id),
            'project_contact_list': project_contact_list
        }

        invites_sent = ''
        no_attachment = []
        no_attachments = ''
        for proj_con in project_contact_list:
            pr_co = ProjectContact.objects.get(id=int(proj_con))
            if pr_co.email_sent_date:
                if pr_co.contact.name:
                    invites_sent += f", {pr_co.contact.name} {pr_co.contact.surname}"
                else:
                    invites_sent += f", Info for {pr_co.contact.company.name}"
            if pr_co.works.email_category_attachment==None:
                print("none!")
                if not f", {pr_co.works.name}" in no_attachment:
                    no_attachment.append(f", {pr_co.works.name}")

        if len(invites_sent) > 3:
            invites_sent = invites_sent[2:]
            messages.warning(request,
                             f"You already sent invites to: {invites_sent}. Are you sure you want to re-send them?")
        if len(no_attachment) > 0:
            no_attachment[0] = no_attachment[0][2:]
            for no_att in no_attachment:
                no_attachments += no_att
            messages.warning(request, f"There is no attachment set for: {no_attachments}. Are you sure you don't need them?")

        return render(request, 'project_contact_message_confirm.html', context)


    elif action == "archive":
        proj_cons = ''
        for project_contact in project_contact_list:
            project_cont = ProjectContact.objects.get(id=int(project_contact))
            project_cont.archivised = True
            project_cont.archivised_date = now()
            project_cont.save()
            proj_cons += f"{project_cont.contact.name} {project_cont.contact.name}, "

        messages.success(request, f'{project_contact_list_len} item(s) archivised!')
        Change_Log.objects.create(category="ProCon", user=request.user,
                                  log=f"Archivised Project Contacts: {proj_cons}", log_date=now())
        return redirect('bbidb:project_contacts', project_id)

    else:
        messages.warning(request, "Something went wrong")
        return redirect('bbidb:project_contacts', project_id)


@login_required
def project_contact_updated(request, project_contact_id):
    project_contact = ProjectContact.objects.get(id=project_contact_id)
    project_contact.date_updated = now()
    project_contact.save()

    if project_contact.contact.name:
        messages.success(request,
                         f'{project_contact.contact.name} {project_contact.contact.surname} in {project_contact.project.name} has been successfully added / updated')
        Change_Log.objects.create(category="ProCon", user=request.user,
                                  log=f"Updated Project Contacts: {project_contact.contact.name} {project_contact.contact.surname}",
                                  log_date=now())
    else:
        messages.success(request,
                         f'Info for {project_contact.contact.company.name} in {project_contact.project.name} has been successfully added / updated')
        Change_Log.objects.create(category="ProCon", user=request.user,
                                  log=f"Updated Project Contacts: Info for {project_contact.contact.company.name} in {project_contact.project.name}",
                                  log_date=now())

    return redirect('bbidb:project_contacts', project_contact.project.id)


@login_required
def project_contact_details(request, project_contact_id):
    project_contact = ProjectContact.objects.get(id=project_contact_id)
    context = {
        'project_contact': project_contact
    }
    return render(request, 'project_contact_details.html', context)


@login_required
def project_contact_message_manage(request, project_contact_id):
    project_contact = ProjectContact.objects.get(id=project_contact_id)
    project = Project.objects.get(id=project_contact.project.id)
    project_works = ProjectContactWorks.objects.get(id=project_contact.works.id)

    context = {
        'project_contact': project_contact,
        'project': project,
        'project_works': project_works
    }
    return render(request, 'project_contact_message_manage.html', context)


@login_required
def project_contact_message_update(request, project_contact_id):
    req = request.POST
    project_contact = ProjectContact.objects.get(id=project_contact_id)
    project = Project.objects.get(id=project_contact.project.id)
    project_works = ProjectContactWorks.objects.get(id=project_contact.works.id)

    # changes for project
    if req['cc']:
        project.email_cc = req['cc']
    else:
        project.email_cc = None
    if req['greeting']:
        project.email_greeting = req['greeting']
    else:
        project.email_greeting = None
    if req['invitation1']:
        project.email_invitation1 = req['invitation1']
    else:
        project.email_invitation1 = None
    if req['invitation2']:
        project.email_invitation2 = req['invitation2']
    else:
        project.email_invitation2 = None
    if req['description1']:
        project.email_description1 = req['description1']
    else:
        project.email_description1 = None
    if req['description2']:
        project.description = req['description2']
    else:
        project.description = None
    if req['attachment2']:
        project.email_attachment2 = req['attachment2']
    else:
        project.email_attachment2 = None
    if req['attachment_full']:
        project.email_attachment_full = req['attachment_full']
    else:
        project.email_attachment_full = None
    if req['note1']:
        project.email_note1 = req['note1']
    else:
        project.email_note1 = None
    if req['note2']:
        project.email_note2 = req['note2']
    else:
        project.email_note2 = None
    if req['note3']:
        project.email_note3 = req['note3']
    else:
        project.email_note3 = None
    if req['general_notes']:
        project.email_general_notes = req['general_notes']
    else:
        project.email_general_notes = None

    # changes for project_contact
    if req['personal_message']:
        project_contact.email_personal_message = req['personal_message']
    else:
        project_contact.email_personal_message = None

    # changes for project_works
    if req['category']:
        project_works.name = req['category']
    else:
        messages.warning(request, 'Works Name is required')
    if req['project_works_message']:
        project_works.email_message = req['project_works_message']
    else:
        project_works.email_message = None
    if req['attachment1']:
        project_works.email_attachment_message = req['attachment1']
    else:
        project_works.email_attachment_message = None
    if req['attachment_category_specific']:
        project_works.email_category_attachment = req['attachment_category_specific']
    else:
        project_works.email_category_attachment = None

    # save changes
    project.save()
    project_contact.save()
    project_works.save()

    Change_Log.objects.create(category="Invite", user=request.user,
                              log=f"Updated Invite in {project.name} for {project_contact.contact.name} {project_contact.contact.surname}",
                              log_date=now())

    return redirect('bbidb:project_contact_message_manage', project_contact_id)


@login_required
def project_contact_details_invite_preview(request, project_contact_id):
    user = request.user
    project_contact = ProjectContact.objects.get(id=project_contact_id)
    project = project_contact.project
    works = project_contact.works

    context = {
        'user': user,
        'project_contact': project_contact,
        'project': project,
        'works': works
    }

    messages.success(request, 'Email has been generated successfully')

    return render(request, 'project_contact_details_invite_preview.html', context)


@login_required
def project_works_manage(request, project_id):
    project = Project.objects.get(id=project_id)
    project_works = ProjectContactWorks.objects.filter(archivised=False, project=project).order_by('name')
    context = {
        'project': project,
        'project_works': project_works
    }
    return render(request, 'project_works_manage.html', context)


@login_required
def project_works_action(request, project_id):
    req = request.POST
    action = str(req['action_no'])
    project = Project.objects.get(id=project_id)
    project_works_list = req.getlist('work')
    project_works_list_len = len(project_works_list)

    if action == "-1":
        messages.warning(request, 'Choose an Action to perform')
        return redirect('bbidb:project_works_manage', project.id)

    elif action == "update":
        proj_works = ''
        for project_work in project_works_list:
            # get the single works package
            work = ProjectContactWorks.objects.get(id=int(project_work))

            # get fields
            if req['works_message' + project_work]:
                work.email_message = req['works_message' + project_work]
            else:
                work.email_message = None
            if req['works_attachment_message' + project_work]:
                work.email_attachment_message = req['works_attachment_message' + project_work]
            else:
                work.email_attachment_message = None
            if req['works_attachment' + project_work]:
                work.email_category_attachment = req['works_attachment' + project_work]
            else:
                work.email_category_attachment = None

            proj_works += f"{work.name}, "

            # save changes
            work.save()

        # inform about the success
        messages.success(request, f'{project_works_list_len} item(s) updated!')
        Change_Log.objects.create(category="ProjWork", user=request.user,
                                  log=f"Updated ProjWorks: {proj_works}",
                                  log_date=now())
        return redirect('bbidb:project_works_manage', project.id)

    elif action == "archive":
        for project_work in project_works_list:
            # get the single works package
            work = ProjectContactWorks.objects.get(id=int(project_work))

            # archivise works package
            work.archivised = True
            work.archivised_date = now()
            work.save()

        # inform about the success
        messages.success(request, f'{project_works_list_len} item(s) archivised!')
        Change_Log.objects.create(category="ProjWork", user=request.user,
                                  log=f"Archivised ProjWorks: {work.name}",
                                  log_date=now())
        return redirect('bbidb:project_works_manage', project.id)

    else:
        # in case something goes wrong
        messages.warning(request, "Something went wrong")
        return redirect('bbidb:project_works_manage', project.id)


@login_required
def archives(request):
    context = {
        'arch_companies': Company.objects.filter(archivised=True),
        'arch_contacts': Contact.objects.filter(archivised=True),
        'arch_projects': Project.objects.filter(archivised=True),
        'arch_project_contacts': ProjectContact.objects.filter(archivised=True),
        'arch_project_works': ProjectContactWorks.objects.filter(archivised=True)
    }
    return render(request, 'archives.html', context)


@login_required
def archive_action(request):
    req = request.POST
    action = str(req['action_no'])
    company_list = req.getlist('arch_company')
    contact_list = req.getlist('arch_contact')
    project_list = req.getlist('arch_project')
    project_contact_list = req.getlist('arch_project_contact')
    project_work_list = req.getlist('arch_project_work')

    if action == "-1":
        messages.warning(request, 'Choose an Action to perform')
        return redirect('bbidb:archives')

    elif action == "restore":

        restored_list = ''
        restored = 0
        for company in company_list:
            comp = Company.objects.get(id=int(company))
            comp.archivised = False
            comp.archivised_date = None
            comp.save()
            restored += 1
            restored_list += f"{comp.name}, "

        for contact in contact_list:
            cont = Contact.objects.get(id=int(contact))
            cont.archivised = False
            cont.archivised_date = None
            cont.save()
            restored += 1
            restored_list += f"{cont.name}, "

        for project in project_list:
            proj = Project.objects.get(id=int(project))
            proj.archivised = False
            proj.archivised_date = None
            proj.save()
            restored += 1
            restored_list += f"{proj.name}, "

        for project_cont in project_contact_list:
            proj_c = ProjectContact.objects.get(id=int(project_cont))
            all_proj_conts = ProjectContact.objects.filter(project=proj_c.project, archivised=False)
            exists = 0
            for proj_cont in all_proj_conts:
                if proj_c.contact == proj_cont.contact:
                    exists = 1

            if exists == 0:
                proj_c.archivised = False
                proj_c.archivised_date = None
                proj_c.save()
                restored += 1
                restored_list += f"{proj_c.contact.name}, "
            else:
                messages.warning(request,
                                 f'{proj_c.contact.name} {proj_c.contact.surname} is already in {proj_c.project.name}')

        for project_work in project_work_list:
            proj_w = ProjectContactWorks.objects.get(id=int(project_work))
            proj_w.archivised = False
            proj_w.archivised_date = None
            proj_w.save()
            restored += 1
            restored_list += f"{proj_w.name}, "

        messages.success(request, f'{restored} item(s) restored!')
        Change_Log.objects.create(category="Archive", user=request.user,
                                  log=f"Restored Items: \n{restored_list}",
                                  log_date=now())
        return redirect('bbidb:archives')

    else:
        messages.warning(request, "Something went wrong")
        return redirect('bbidb:archives')


@login_required
def change_logs(request):
    logs = Change_Log.objects.all()
    context = {
        'logs': logs
    }

    return render(request, 'logs.html', context)
