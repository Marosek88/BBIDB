from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.urls import path

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    # url(r'^register/$', user_views.register, name='register'),
    url(r'^profile/$', user_views.profile, name='profile'),
    url(r'^login/$', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    url(r'^logout/$', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(template_name='users/password_reset.html'),
        name='password_reset'),
    url(r'^password_reset/done/$',
        auth_views.PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'),
        name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password_reset_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),
         name='password_reset_complete'),

    url(r'^', include('bbidb_app.urls')),
    url(r'^', include('users.urls')),
    url(r'^', include(''
                      '.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
