from django.conf.urls import url
from django.views.generic import TemplateView

from .views import TermSearch


urlpatterns = [
    url(r'^presentation$', TemplateView.as_view(template_name='semantic/meurgorf/presentation.html')),
    url(r'^sources$', TemplateView.as_view(template_name='semantic/meurgorf/sources.html')),
    url(r'^abrev$', TemplateView.as_view(template_name='semantic/meurgorf/abrev.html')),
    url(r'^(?P<term_id>\d+)?$', TermSearch.as_view(), name='term')
]
