from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('create/', views.create, name='create'),
    path('create/<int:ticket_id>/', views.create, name='create'),
    path('edit/<int:review_id>/', views.edit, name='edit'),
    path('me/', views.user_posts, name="me")
]