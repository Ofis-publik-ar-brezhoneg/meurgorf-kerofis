from rest_framework import routers

from commun.views import UsersView
from commun.views import BooksView

from meurgorf.views import DerivedFormView
from meurgorf.views import GrammaticalCategoryView
from meurgorf.views import HistoricalOccurrenceView
from meurgorf.views import StatView as MeurgorfStatView
from meurgorf.views import TermView
from meurgorf.views import VariantView
from meurgorf.views import MeurgorfExportView

api = routers.SimpleRouter()
api.register(r'users', UsersView)
api.register(r'books', BooksView)
api.register(r'categories', GrammaticalCategoryView)
api.register(r'derived_forms', DerivedFormView)
api.register(r'historical_occurrences', HistoricalOccurrenceView)
api.register(r'variants', VariantView)
api.register(r'terms', TermView)
api.register(r'stats/meurgorf', MeurgorfStatView)
api.register(r'export/meurgorf', MeurgorfExportView)
api.trailing_slash = '/?'
