from django.urls import path
from . import views


urlpatterns = [
  # renders
    path('', views.index),
    path('wall', views.wall),
    
    # redirects
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('wall/create', views.create_message),
    path('wall/comment/<int:message_id>', views.create_comment),
    path('wall/delete/<int:message_id>', views.delete_message),
    path('wall/comment/delete/<int:comment_id>', views.delete_comment),
]
