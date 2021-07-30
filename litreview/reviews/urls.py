from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('create/', views.create, name='create'),
    path('create/<int:ticket_id>', views.create, name='create')
]