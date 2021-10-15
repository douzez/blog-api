from django.urls import path

from users.views import CreateUserView, CreateTokenView, ManageUserView

app_name = 'user'

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create'),
    path('token/', CreateTokenView.as_view(), name='token'),
    path('mu/', ManageUserView.as_view(), name='mu')
]
