from django.conf.urls import url
from . import views

app_name = 'bbidb'

urlpatterns = [
    # /
    url(r'^$', views.index, name='index'),

    # /import/
    url(r'^import_many/$', views.import_multiple, name='import_multiple'),
    # /import_action
    url(r'^import_action/$', views.import_action, name='import_action'),

    # /companies/
    url(r'^companies/$', views.companies, name='companies'),
    # /company_details/<company_id>/
    url(r'^company_details/(?P<company_id>[0-9]+)/$', views.company_details, name='company_details'),
    # company/add/
    url(r'^company/add/$', views.CompanyCreate.as_view(), name='company_add'),
    # company/<company_id>/
    url(r'^company/(?P<pk>[0-9]+)/$', views.CompanyUpdate.as_view(), name='company_update'),
    # /company_updated/<company_id>
    url(r'^company_updated/(?P<company_id>[0-9]+)/$', views.company_updated, name='company_updated'),
    # # company/<company_id>/delete
    # url(r'^company/(?P<pk>[0-9]+)/delete/$', views.CompanyDelete.as_view(), name='company_delete'),
    # company/<company_id>/archive
    # url(r'^company/(?P<company_id>[0-9]+)/archive/$', views.company_archive, name='company_archive'),
    # /company_action/
    url(r'^company_action/$', views.company_action, name='company_action'),

    # /contacts/
    url(r'^contacts/', views.contacts, name='contacts'),
    # /contact_details/<contact_id>
    url(r'^contact_details/(?P<contact_id>[0-9]+)/$', views.contact_details, name='contact_details'),
    # /contact/add
    url(r'^contact/add/$', views.ContactCreate.as_view(), name='contact_add'),
    # contact/<contact_id>/
    url(r'^contact/(?P<pk>[0-9]+)/$', views.ContactUpdate.as_view(), name='contact_update'),
    # /contact_updated/<contact_id>
    url(r'^contact_updated/(?P<contact_id>[0-9]+)/$', views.contact_updated, name='contact_updated'),
    # # /contact/<contact_id>/delete
    # url(r'^contact/(?P<pk>[0-9]+)/delete$', views.ContactDelete.as_view(), name='contact_delete'),
    # /contact/<contact_id>/archive
    # url(r'^contact/(?P<contact_id>[0-9]+)/archive$', views.contact_archive, name='contact_archive'),
    # /contact_action/
    url(r'^contact_action/$', views.contact_action, name='contact_action'),

    # /projects/
    url(r'^projects/', views.projects, name='projects'),
    # /project/add
    url(r'^project/add/$', views.ProjectCreate.as_view(), name='project_add'),
    # /project/<contact_id>/
    url(r'^project/(?P<pk>[0-9]+)/$', views.ProjectUpdate.as_view(), name='project_update'),
    # /project_updated/<project_id>
    url(r'^project_updated/(?P<project_id>[0-9]+)/$', views.project_updated, name='project_updated'),
    # # /project/<contact_id>/delete
    # url(r'^project/(?P<pk>[0-9]+)/delete$', views.ProjectDelete.as_view(), name='project_delete'),
    # # /project/<contact_id>/archive
    # url(r'^project/(?P<project_id>[0-9]+)/archive$', views.project_archive, name='project_archive'),
    # /project_action/
    url(r'^project_action/$', views.project_action, name='project_action'),

    # /project_contacts/<project_id>
    url(r'^project_contacts/(?P<project_id>[0-9]+)/$', views.project_contacts, name='project_contacts'),
    # /project_contact_details/<project_id>/<project_contact_id>
    url(r'^project_contact_details/(?P<project_contact_id>[0-9]+)/$', views.project_contact_details,
        name='project_contact_details'),
    # /project_contact/add
    url(r'^project_contact/add/$', views.ProjectContactCreate.as_view(), name='project_contact_add'),
    # /project_contact/<contact_id>/
    url(r'^project_contact_update/(?P<pk>[0-9]+)/$', views.ProjectContactUpdate.as_view(),
        name='project_contact_update'),
    # /project_contact_updated/<project_contact_id>
    url(r'^project_contact_updated/(?P<project_contact_id>[0-9]+)/$', views.project_contact_updated,
        name='project_contact_updated'),
    # # /project_contact/<contact_id>/delete
    # url(r'^project_contact_details/(?P<pk>[0-9]+)/delete$', views.ProjectContactDelete.as_view(),
    #     name='project_contact_delete'),
    # # /project_contact/<contact_id>/delete
    # url(r'^project_contact_details/(?P<project_contact_id>[0-9]+)/archive$', views.project_contact_archive,
    #     name='project_contact_archive'),
    # /project_contact_action/
    url(r'^project_contact_action/$', views.project_contact_action, name='project_contact_action'),
    # /project_contact/<project_contact_id>/message_manage
    url(r'^project_contact_details/(?P<project_contact_id>[0-9]+)/message_manage$',
        views.project_contact_message_manage,
        name='project_contact_message_manage'),
    url(r'^project_contact_details/(?P<project_contact_id>[0-9]+)/message_update$',
        views.project_contact_message_update,
        name='project_contact_message_update'),
    # /project_contact/<project_contact_id>/render_email
    url(r'^project_contact_details/(?P<project_contact_id>[0-9]+)/invite_preview/$',
        views.project_contact_details_invite_preview,
        name='project_contact_details_invite_preview'),

    # /project_contacts/<project_id>/add_works
    url(r'^project_contacts/(?P<project_id>[0-9]+)/add_works/$', views.ProjectContactWorksCreate.as_view(),
        name='project_contact_works_create'),
    # /project_contacts/<project_id>/<project_contact_works_id>
    # url(r'^project_contacts/(?P<project_id>[0-9]+)/(?P<pk>[0-9]+)/$', views.ProjectContactWorksUpdate.as_view(),
    #     name='project_contact_works_update'),
    # /project_contacts/<project_id>/project_works_manage
    url(r'^project_contacts/(?P<project_id>[0-9]+)/project_works_manage/$', views.project_works_manage,
        name='project_works_manage'),
    # /project_contacts/<project_id>/project_works_action
    url(r'^project_contacts/(?P<project_id>[0-9]+)/project_works_action/$', views.project_works_action,
        name='project_works_action'),

    # /archives/
    url(r'^archives/$', views.archives, name='archives'),
    # / archive_action/
    url(r'^archive_action/$', views.archive_action, name='archive_action'),

    url(r'^change_log.$', views.change_logs, name='change_logs')
]
