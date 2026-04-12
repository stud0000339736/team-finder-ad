from django.urls import path
from .views import register, login_2, logout_2, user_detail, edit_user, change_password, users_list


app_name = 'users'

urlpatterns = [
    # base rllc
    path('register/', register, name='register'),
    path('login/', login_2, name='login'),
    path('logout/', logout_2, name='logout'),
    path('change-password/', change_password, name='change-password'),
    # for users
    path('<int:pk>/', user_detail, name='profile'),
    path('edit-profile/', edit_user, name='edit-profile'),
    path('list/', users_list, name='users-list')
]
