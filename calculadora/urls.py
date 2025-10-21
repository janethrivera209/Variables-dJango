from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),          # página principal
    path('evaluate/', views.evaluate, name='evaluate'),  # evalúa expresiones
]
