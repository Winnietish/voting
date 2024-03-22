from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views
from django.contrib.auth import views as auth_views

from .forms import StudentLoginForm

urlpatterns = [
    path("", views.index, name="index"),
    path("register/", views.register, name="register"),
    path('login/', auth_views.LoginView.as_view(authentication_form=StudentLoginForm,template_name='login.html'), name='login'),
    path("logout/", views.logout_view, name="logout"),
    path("results/",views.results,name='results'),
    path('vote/',views.vote,name='vote'),
    path('submit_vote/',views.submit_vote,name='submit_vote'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)