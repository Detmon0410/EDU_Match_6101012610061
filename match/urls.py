from django.urls import path,include
from match.views import sign_up_view , profile_view
from . import views
from django.contrib.auth import views as auth_views
from django.contrib import admin
from django.conf import settings
from django.contrib.staticfiles.urls import static

app_name = 'match'
urlpatterns = [
    # ex: /match/
    path('chat/', include('chat.urls')),
    path('', views.home, name='home'),
    path('signup/',views.sign_up_view, name='SignUpView'),
    path('profile/', views.profile_view, name='ProfileView'),
    path('view_profile/<str:name>', views.view_other_profile, name='view_profile'),
    path('view_profile_R/<str:name>', views.view_r_profile, name='view_profile_R'),
    path('friendmatched/', views.friend_matched, name='friendmatched'),
    path('friendprofile/<str:name>', views.friend_profile, name='friendprofile'),
    path('unmatched/<str:name>', views.un_friend_matched, name='unmatched'),
    path('acceptmatch/<str:name>', views.accept_match, name='acceptM'),
    path('declinematch/<str:name>', views.de_cline_match, name='declineM'),
    path('matching/<str:name>', views.matching, name='matching'),
    path('request_match/', views.request_match, name='request_match'),
    path('unmatching/<str:name>', views.un_matching, name='unmatching'),
    path('accounts/',include('django.contrib.auth.urls')),
    path('profile_add_subject/', views.profile_add_subject,name='profile_add_subject'),
    path('add_subject/', views.add_subject, name='add_subject'),
    path('write_review/<str:profilename>', views.write_review, name='write_review'),
    path('write_review_matched/<str:profilename>', views.write_review_matched, name='write_review_matched'),
    path('clean_model/', views.clean_model, name='clean'),
    path('search/', views.searching, name='search'),
    path('about_app', views.about_app, name='about_app'),
    path('about_group', views.about_group, name='about_group'),
    path('help', views.help_app, name='help'),
    path('accounts/change_password/',
        auth_views.PasswordChangeView.as_view(
            template_name='registration/change_password.html',
            success_url='/accounts/change_password/done'
        ),
        name='change_password'
    ),
    path('accounts/change_password/done', views.change_password_done, name='change_password_done'),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#path('profile/<int:pk>/', ProfileView.as_view(), name='profile'),
#path('signup/',SignUpView.as_view(), name='signup'),
