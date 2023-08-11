from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
                  path("admin/", admin.site.urls),
                  path('email-attach/', include('emailattach.urls')),
                  path('baseviews/', include('djangobaseviews.urls')),
                  path('genericviews/', include('djangogenericviews.urls')),
                  path('complexqueries/', include('complexqueries.urls')),
                  path('modelrelationship/', include('modelrelationship.urls')),
                  path('mastering-django/',
                       include(('mastering_django.urls', 'mastering_django'), namespace='mastering_django')),
                  
                  path("__debug__/", include("debug_toolbar.urls")),  # for debug tooler
              ]


# when debug = true

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
