from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("about-evan/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("faqs/<str:service_type>", views.faqs, name="faqs"),
]
