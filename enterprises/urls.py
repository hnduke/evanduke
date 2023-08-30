from django.urls import path

from . import views
from .views import ContactView

urlpatterns = [
    path("", views.index, name="index"),
    path("about-evan/", views.about, name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("thank-you/", views.thank_you, name="thank-you"),
    path("faqs/<str:service_type>", views.faqs, name="faqs"),
]
