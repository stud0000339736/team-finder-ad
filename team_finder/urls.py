from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from .views import main_page


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_page),
    path('users/', include('users.urls')),
    path('projects/', include('projects.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# if settings.DEBUG:
#     urlpatterns += [
#         path('__debug__/', include('debug_toolbar.urls')),
# ]
