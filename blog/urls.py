from django.urls import path
from .views import (
    PostListView, 
    PostDetailView, 
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    UserPostListView,
    image_like,
)

app_name = 'blog'

urlpatterns = [
    path('',PostListView, name='post-list'),
    path('tag/<slug:tag_slug>/',PostListView, name='post-list-by-tag'),
    path('search/',PostListView, name='post-by-search'),
    path('<int:pk>/',PostDetailView,name='post-detail'),
    path('user/<str:username>', UserPostListView, name='user-posts'), 
    path('<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),    
    path('new/', PostCreateView.as_view(),name='post-create'),
    path('like/', image_like, name='like'),
]
