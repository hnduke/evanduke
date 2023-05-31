from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('about-evan/', views.about, name='about'),
    path('lessons/', views.lessons, name='lessons'),
    path('business-consultations/', views.business, name='business'),
    path('performances/', views.performances, name='performances'),
    path('research-projects/', views.research, name='research'),
    path('contact/', views.contact, name='contact'),
]
