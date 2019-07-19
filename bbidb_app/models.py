from django.utils.timezone import now
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Category(models.Model):
    class Meta:
        verbose_name_plural = 'categories'
        ordering = ['name']

    name = models.CharField(max_length=100, blank=True, unique=True)
    archivised = models.BooleanField(default=False)
    archivised_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.name


class Company(models.Model):
    class Meta:
        verbose_name_plural = 'companies'
        ordering = ['name']

    name = models.CharField(max_length=100, unique=True)
    head_address = models.TextField(null=True, blank=True)
    head_phone = models.CharField(max_length=30, null=True, blank=True)
    head_email = models.EmailField(null=True, blank=True)
    website = models.URLField(null=True, blank=True)
    company_logo = models.FileField(blank=True)
    date_added = models.DateField(null=True, blank=True, default=now())
    added_by = models.CharField(max_length=50, null=True, blank=True)
    date_updated = models.DateField(null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    archivised = models.BooleanField(default=False)
    archivised_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('bbidb:company_updated', kwargs={'company_id': self.id})

    def __str__(self):
        return self.name


class Contact(models.Model):
    class Meta:
        ordering = ['name']

    company = models.ForeignKey(Company, on_delete=models.DO_NOTHING)
    category = models.ManyToManyField(Category)
    name = models.CharField(max_length=100, null=True, blank=True )
    surname = models.CharField(max_length=100, null=True, blank=True)
    role = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=100, null=True, blank=True)
    mobile = models.CharField(max_length=100, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    date_added = models.DateField(null=True, blank=True, default=now())
    added_by = models.CharField(max_length=100, null=True, blank=True)
    date_updated = models.DateField(null=True, blank=True)
    updated_by = models.CharField(max_length=100, null=True, blank=True)
    date_used = models.DateField(default=now())
    remarks = models.TextField(null=True, blank=True)
    archivised = models.BooleanField(default=False)
    archivised_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('bbidb:contact_updated', kwargs={'contact_id': self.id})

    def __str__(self):
        return str(self.name) + ' ' + str(self.surname) + ' - ' + str(self.company.name)


class Project(models.Model):
    class Meta:
        ordering = ['name']

    name = models.CharField(max_length=250)
    status = models.BooleanField(blank=True, default=True)
    description = models.TextField(null=True, blank=True)
    tender_submission = models.DateField(null=True, blank=True)
    contract_start = models.DateField(null=True, blank=True)
    date_added = models.DateField(null=True, blank=True, default=now())
    added_by = models.CharField(max_length=50, null=True, blank=True)
    date_updated = models.DateField(null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    email_cc = models.TextField(null=True, blank=True, default="paul.bolger@balfourbeatty.com; matthew.fudala@balfourbeatty.com")
    email_quotation_deadline = models.DateField(null=True, blank=True)
    email_greeting = models.CharField(max_length=50, null=True, blank=True, default="Hello")
    email_invitation1 = models.TextField(null=True, blank=True,
                                         default="We are currently preparing a tender for the project:")
    email_invitation2 = models.TextField(null=True, blank=True,
                                         default=" and we would like to invite you to submit your most competitive  quotation for")
    email_description1 = models.TextField(null=True, blank=True,
                                          default="Please see the short description of the project below:")
    email_attachment2 = models.TextField(null=True, blank=True,
                                         default="To see a full tender documentation, please visit the link below:")
    email_attachment_full = models.TextField(null=True, blank=True)
    email_note1 = models.TextField(null=True, blank=True, default="Please note the following:")
    email_note2 = models.TextField(null=True, blank=True, default="- Please submit your tenders no later than 5pm on")
    email_note3 = models.TextField(null=True, blank=True)
    email_general_notes = models.TextField(null=True, blank=True,
                                           default="- Your tender must be fixed price and remain open for acceptance for a period of six months from the date of return or 14 days greater than the validity period stated in the Main Contract, whichever is the longer.\n- The sub-contractor is responsible for obtaining all further information (and will be deemed to have done so) in order to ensure the sufficiency of your tender.\n- The information made available in connection with this invitation to tender is confidential and must not be divulged beyond the degree necessary to prepare your tender.\n- Works must be carried out in accordance with Balfour Beatty Subcontractors Health, Safety, Environment, Quality and Sustainability Conditions.")
    boq = models.FileField(blank=True)
    archivised = models.BooleanField(default=False)
    archivised_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('bbidb:project_updated', kwargs={'project_id': self.id})

    def __str__(self):
        return self.name


class ProjectContactWorks(models.Model):
    class Meta:
        verbose_name_plural = 'project contact works'
        ordering = ['name']

    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    category = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    email_message = models.TextField(null=True, blank=True)
    email_attachment_message = models.TextField(null=True, blank=True, default="Please see an extract from BoQ and other documents relevant to your works in a link below:")
    email_category_attachment = models.TextField(null=True, blank=True)
    archivised = models.BooleanField(default=False)
    archivised_date = models.DateField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('bbidb:project_contacts', kwargs={'project_id': self.project.id})

    def __str__(self):
        return str(self.project.name) + ' - ' + str(self.name)


class ProjectContact(models.Model):
    project = models.ForeignKey(Project, on_delete=models.DO_NOTHING)
    contact = models.ForeignKey(Contact, on_delete=models.DO_NOTHING)
    works = models.ForeignKey(ProjectContactWorks, on_delete=models.DO_NOTHING, null=True, blank=True)
    attachment = models.FileField(null=True, blank=True)
    date_added = models.DateField(null=True, blank=True)
    added_by = models.CharField(max_length=50, null=True, blank=True)
    date_updated = models.DateField(null=True, blank=True)
    updated_by = models.CharField(max_length=50, null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    email_sent_date = models.DateTimeField(null=True, blank=True)
    will_price_date = models.DateTimeField(null=True, blank=True)
    not_interested_date = models.DateTimeField(null=True, blank=True)
    requires_clarification_date = models.DateTimeField(null=True, blank=True)
    quotation_received = models.DateTimeField(null=True, blank=True)
    email_personal_message = models.TextField(null=True, blank=True)
    assigned_to = models.ForeignKey(User, on_delete=models.DO_NOTHING, null=True, blank=True)
    archivised = models.BooleanField(default=False)
    archivised_date = models.DateTimeField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('bbidb:project_contact_updated', kwargs={'project_contact_id': self.id})

    def __str__(self):
        return str(self.project.name) + ' - ' + str(self.contact.company.name) + ' - ' + str(
            self.contact.name) + ' ' + str(self.contact.surname)


class Change_Log(models.Model):
    category = models.CharField(max_length=20)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    log = models.TextField(null=True, blank=True)
    log_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return str(self.log_date) + ' - ' + str(self.user.first_name) + ' ' + str(self.user.first_name) + ' - ' + str(self.log)