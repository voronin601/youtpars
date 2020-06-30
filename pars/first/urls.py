from django.urls import path, include
from .views import start_pars, vivod

urlpatterns = [
    path('start/', start_pars),
    path('', vivod)
]
