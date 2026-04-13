from django.urls import path

from projects import views

app_name = 'projects'

urlpatterns = [
    path('list/', views.project_list, name='project_list'),
    path('create-project/', views.create_project, name='create_project'),
    path('favorites/', views.get_favorites, name='favorites'),
    path('<int:project_id>/toggle-favorite/', views.toggle_favorite, name='toggle_favorite'),
    path('<int:project_id>/complete/', views.project_complete, name='complete'),
    path('<int:project_id>/', views.project_detail, name='project_detail'),
    path('<int:project_id>/edit/', views.project_edit, name='project_edit'),
    path('<int:project_id>/toggle-participate/', views.project_toggle, name='project_toggle')
]
