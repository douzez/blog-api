from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('tags', views.AllTags.as_view(), name='all-tags'),
    path('tags/create/', views.TagView.as_view(), name='create-tag'),
    path('tags/<slug:tag_slug>/', views.TagDetail.as_view(), name='tag-detail'),
    path('tags/update/<slug:tag_slug>/',
         views.TagView.as_view(), name='update-tag'),
    path('tags/delete/<slug:tag_slug>/',
         views.TagView.as_view(), name='delete-tag'),
    path('posts/', views.AllPosts.as_view(), name='all_posts'),
    path('posts/<slug:post_slug>/', views.PostDetail.as_view(), name='post-detail'),
]
