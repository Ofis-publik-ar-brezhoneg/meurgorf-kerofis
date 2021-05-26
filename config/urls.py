from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.conf.urls.i18n import i18n_patterns


from .api import api
from meurgorf import urls as meurgorf_urls
from kerofis import urls as kerofis_urls
from commun import urls as skridaozer_urls


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^skridaozer/', include(skridaozer_urls, namespace='skridaozer')),
]

if settings.DEBUG:
    # Media urls for development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    path('', TemplateView.as_view(template_name='semantic/index.html')),
    url(r'^meurgorf/', include(meurgorf_urls)),
    url(r'^kerofis/', include(kerofis_urls))
)
