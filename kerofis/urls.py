from django.conf.urls import url
from django.views.generic import TemplateView

from .views import KerofisSearch
from .views import KerofisRedirect

urlpatterns = [
    url(
        r'^presentation$',
        TemplateView.as_view(template_name='semantic/kerofis/presentation.html'),
        name='kerofis-presentation'
    ),
    url(
        r'^savoir',
        TemplateView.as_view(template_name='semantic/kerofis/savoir.html'),
        name='kerofis-savoir'
    ),
    # url(r'^$', TemplateView.as_view(template_name='semantic/kerofis/index.html'), name='kerofis')
    url(r'^(?P<location_id>\d+)?$', KerofisSearch.as_view(), name='kerofis'),
    url(r'^city/(?P<location_name>[\w \[\]]+)?$', KerofisRedirect.as_view(), name='kerofis-city')
]
