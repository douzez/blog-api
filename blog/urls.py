from django.urls import path

from blog import views

app_name = 'blog'

urlpatterns = [
    path('tags', views.AllTags.as_view(), name='all_tags'),
    path('tags/<slug:tag_slug>', views.TagDetail.as_view(), name='tag-detail'),
    path('posts', views.AllPosts.as_view(), name='all_posts'),
    path('posts/<slug:post_slug>', views.PostDetail.as_view(), name='post-detail'),
]
