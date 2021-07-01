from django.urls import path
from . import views


urlpatterns = [
    path('', views.test, name='test'),
    path('patient/', views.patient, name='patient'),
    path('visit/', views.visit, name='visit'),
    path('search/', views.search, name='search'),
    path('onlyOne/', views.onlyOne, name='onlyOne'),
    
]