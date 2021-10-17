from django.urls import path

from users import views

app_name = 'user'

urlpatterns = [
    path('create/', views.CreateUser.as_view(), name='create'),
    path('token/', views.CreateToken.as_view(), name='token'),
    path('mu/', views.ManageUser.as_view(), name='mu')
]
