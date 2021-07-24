from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('signup/', views.signup, name="signup"),
    path('logout/', views.auth_logout, name="logout"),
    path('follows/', views.follows, name="follows"),
    path('unfollow/<int:user_id>/', views.delete_follow, name="unfollow")
]