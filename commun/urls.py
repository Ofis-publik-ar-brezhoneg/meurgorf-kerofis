from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from commun.views import SkridaozerBookView
from commun.views import SkridaozerDeleteBookView
from commun.views import SkridaozerAddBookView
from meurgorf.views import SkridaozerMeurgorfTermView
from meurgorf.views import SkridaozerMeurgorfAddTermView
from meurgorf.views import SkridaozerMeurgorfStatView
from meurgorf.views import SkridaozerMeurgorfExportView
from meurgorf.views import SkridaozerMeurgorfSearchView
from meurgorf.views import SkridaozerMeurgorfAjaxView
from kerofis.views import SkridaozerKerofisLocationView
from kerofis.views import SkridaozerKerofisAddLocationView
from kerofis.views import SkridaozerKerofisStatView
from kerofis.views import SkridaozerKerofisExportView
from kerofis.views import SkridaozerKerofisSearchView
from kerofis.views import SkridaozerKerofisInformantView
from kerofis.views import SkridaozerKerofisExportInfoView
from kerofis.views import SkridaozerKerofisAjaxView
from kerofis.views import SkridaozerKerofisTemplateView


class LoggedMainView(LoginRequiredMixin, TemplateView):
    pass


app_name = 'skridaozer'
urlpatterns = [
    url(r'^$', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html')),
    url(r'^mammennoù/(?P<book_id>\d+)?$', SkridaozerBookView.as_view(), name='mammennou'),
    url(r'^mammennoù_lemel/(?P<book_id>\d+)?$', SkridaozerDeleteBookView.as_view(), name='mammennou_lemel'),
    url(r'^mammennoù_ouzhpennan/(?P<book_id>\d+)?$', SkridaozerAddBookView.as_view(), name='mammennou_ouzhpennan'),

    url(r'meurgorf/klask', SkridaozerMeurgorfSearchView.as_view(), name='meurgorf_klask'),
    url(r'meurgorf/ouzhpennan', SkridaozerMeurgorfAddTermView.as_view(), name='meurgorf_ouzhpennan'),
    url(r'meurgorf/etrefas/(?P<term_id>\d+)?$', SkridaozerMeurgorfTermView.as_view(), name='meurgorf_etrefas'),
    url(r'meurgorf/stadegoù', SkridaozerMeurgorfStatView.as_view(), name='meurgorf_stadegou'),
    url(r'meurgorf/ezporzhiañ', SkridaozerMeurgorfExportView.as_view(), name='meurgorf_ezporzhian'),
    url(r'meurgorf/ajax/(?P<term_id>\d+)$', SkridaozerMeurgorfAjaxView.as_view(), name='meurgorf_ajax'),

    url(r'kerofis/klask', SkridaozerKerofisSearchView.as_view(), name='kerofis_klask'),
    url(r'kerofis/ouzhpennan', SkridaozerKerofisAddLocationView.as_view(), name='kerofis_ouzhpennan'),
    url(r'kerofis/titourer/(?P<informant_id>\d+)?$', SkridaozerKerofisInformantView.as_view(), name='kerofis_titourer'),
    url(r'kerofis/stadegoù', SkridaozerKerofisStatView.as_view(), name='kerofis_stadegou'),
    url(r'kerofis/Levrigoù', SkridaozerKerofisExportInfoView.as_view(), name='kerofis_levrigou'),
    url(r'kerofis/etrefas/(?P<location_id>\d+)?$', SkridaozerKerofisLocationView.as_view(), name='kerofis_etrefas'),
    url(r'kerofis/ezporzhiañ', SkridaozerKerofisExportView.as_view(), name='kerofis_ezporzhian'),
    url(r'kerofis/ajax/(?P<location_id>\d+)$', SkridaozerKerofisAjaxView.as_view(), name='kerofis_ajax'),
    url(r'kerofis/view/(?P<template>\w+)/(?P<id>\d+)?$', SkridaozerKerofisTemplateView.as_view(), name='kerofis_view')
]
