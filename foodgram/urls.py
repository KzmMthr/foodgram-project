from django.conf import settings
from django.conf.urls import handler400, handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from . import views

handler404 = 'foodgram.views.page_not_found'  # noqa
handler500 = 'foodgram.views.server_error'  # noqa
handler400 = 'foodgram.views.page_bad_request'  # noqa


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('api/', include('api.urls')),
    path('', include('recipes.urls')),
]


urlpatterns += [
    path('author/', views.AuthorStaticPage.as_view()),
    path('tech/', views.TechStaticPage.as_view()),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
