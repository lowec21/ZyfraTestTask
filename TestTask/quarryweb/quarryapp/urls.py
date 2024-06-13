from django.urls import path
from .views import main_index

app_name = 'quarryapp'

urlpatterns = [
    path('', main_index, name='index'),
]