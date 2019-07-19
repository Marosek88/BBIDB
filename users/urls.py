from django.conf.urls import url
from django.contrib.auth import views as auth_views

from users import views as user_views
from django.urls import path

app_name = 'users'

urlpatterns = [
    # url(r'^register/$', user_views.register, name='register'),
    # url(r'^profile/$', user_views.profile, name='profile'),
    # url(r'^login/$', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    # url(r'^logout/$', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    # url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
    #     name='password_reset'),
    # url(r'^password_reset/done/$',
    #     auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
    #     name='password_reset_done'),
    # path('password_reset_confirm/<uidb64>/<token>/',
    #      auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
    #      name='password_reset_confirm'),
    # path('password_reset_complete/',
    #      auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
    #      name='password_reset_complete'),
    ]
