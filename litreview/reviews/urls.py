from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('ask/', views.ask, name='ask'),
    path('create/', views.create, name='create'),
    path('create/<int:ticket_id>/', views.create, name='create'),
    path('edit/<int:review_id>/', views.edit, name='edit'),
    path(
        'edit_ticket/<int:review_id>/',
        views.edit_ticket,
        name='edit_ticket'
    ),
    path(
        'delete_review/<int:review_id>/',
        views.delete_review,
        name='delete_review'
    ),
    path(
        'delete_ticket/<int:ticket_id>/',
        views.delete_ticket,
        name='delete_ticket'
    ),
    path('me/', views.user_posts, name="me")
]
