from django.urls import path

from users.views import (change_password, edit_user, login_user, logout_user,
                         register, user_detail, users_list)

app_name = 'users'

urlpatterns = [
    # base rllc
    path('register/', register, name='register'),
    path('login/', login_user, name='login'),
    path('logout/', logout_user, name='logout'),
    path('change-password/', change_password, name='change-password'),
    # for users
    path('<int:user_id>/', user_detail, name='profile'),
    path('edit-profile/', edit_user, name='edit-profile'),
    path('list/', users_list, name='users-list')
]
