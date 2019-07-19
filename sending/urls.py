from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from sending import views as sending_views
from django.urls import path

app_name = 'sending'

urlpatterns = [
    # path('send_test/<project_contact_id>', sending_views.send_mail_test, name='send_test'),
    path('project_contact/<project_contact_id>/sending_invite', sending_views.sending_invite, name='sending_invite'),

    path('sending_bulk_invites/<project_id>', sending_views.sending_bulk_invite, name='sending_bulk_invite'),
]
