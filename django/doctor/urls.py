from django.urls import path
from .views import HomeTemplateView, AppointmentTemplateView, ManageAppointmentTemplateView
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin




admin.site.site_header="AlSamad's Dashboard"
admin.site.site_title="Dashboard"
admin.site.index_title="Exclusive Admin Commands"
urlpatterns = [

    path("", HomeTemplateView.as_view(), name="home"),
    path("make-an-appointment", AppointmentTemplateView.as_view(), name="appointment"),
    path("manage-appointments", ManageAppointmentTemplateView.as_view(), name="manage"),
    path("online-reporting", views.onlineReporting, name="online-reporting"),
    path("search_results", views.searchResults, name="search_results"),
    path("login", views.login, name="login"),
    path("contact", views.contact, name="contact"),
    path("signup", views.signUp, name="signup"),
    path("handleSignUp", views.handleSignUp, name="handleSignUp"),
    path("handleLogIn", views.handleLogIn, name="handleLogIn"),
    path("handelLogout", views.handelLogout, name="handelLogout"),
    path("about", views.about, name="about"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
