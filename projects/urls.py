from django.urls import path
from . import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('create-project/', views.create_project, name='create_project'),
    path('favorites/', views.get_favorites, name='favorites'),
    path('<int:pk>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:pk>/complete/', views.project_complete, name='complete'),
    path('<int:pk>/', views.project_detail, name='project_detail'),
    path('<int:pk>/edit/', views.project_edit, name='project_edit'),
    path('<int:pk>/toggle-participate/', views.project_toggle, name='project_toggle')
]
