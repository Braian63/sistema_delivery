
from django.urls import path
from .views import exibir_lanchonete  

urlpatterns = [
    path('exibir_lanchonete', exibir_lanchonete, name='exibir_lanchonete'),
]