from django.conf import settings
from django.conf.urls import url
from django.urls import include, path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from .api import api
from meurgorf import urls as meurgorf_urls


urlpatterns = [
    path('accounts/', include('django.contrib.auth.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
]

if settings.DEBUG:
    # Media urls for development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


class MainView(TemplateView):

    def get_context_data(self, **kwargs):
        context = super(MainView, self).get_context_data(**kwargs)
        context['DEBUG'] = settings.USE_NPM

        return context


class LoggedMainView(LoginRequiredMixin, MainView):
    pass


# App: Vue routing
urlpatterns += [
    url(r'^skridaozer', LoggedMainView.as_view(template_name='main.html')),
    url(r'^$', TemplateView.as_view(template_name='semantic/index.html')),
    url(r'^meurgorf/', include(meurgorf_urls))
]
