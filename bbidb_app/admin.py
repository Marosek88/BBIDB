from django.contrib import admin

from bbidb_app.models import Category, Company, Contact, Project, ProjectContact, ProjectContactWorks, Change_Log

admin.site.register(Category)
admin.site.register(Company)
admin.site.register(Contact)
admin.site.register(Project)
admin.site.register(ProjectContact)
admin.site.register(ProjectContactWorks)
admin.site.register(Change_Log)
