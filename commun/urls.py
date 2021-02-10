from django.conf.urls import url
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from meurgorf.views import SkridaozerTermView



class LoggedMainView(LoginRequiredMixin, TemplateView):
    pass


app_name = 'skridaozer'
urlpatterns = [
    url(r'^$', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html')),
    url(r'^mammennoù$', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html'), name='mammennou'),

    url(r'meurgorf/klask', SkridaozerTermView.as_view(), name='meurgorf_klask'),
    url(r'meurgorf/etrefas', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html'), name='meurgorf_etrefas'),
    url(r'meurgorf/stadegoù', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html'), name='meurgorf_stadegou'),
    url(r'meurgorf/ezporzhiañ', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html'), name='meurgorf_ezporzhian'),

    url(r'kerofis/klask', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html'), name='kerofis_klask'),
    url(r'kerofis/titourer', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html'), name='kerofis_titourer'),
    url(r'kerofis/stadegoù', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html'), name='kerofis_stadegou'),
    url(r'kerofis/Levrigoù', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html'), name='kerofis_levrigou'),
    url(r'kerofis/etrefas', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html'), name='kerofis_etrefas'),
    url(r'kerofis/ezporzhiañ', LoggedMainView.as_view(template_name='semantic/skridaozer/index.html'), name='kerofis_ezporzhian'),
]
