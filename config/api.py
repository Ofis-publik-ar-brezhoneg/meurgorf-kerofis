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
from meurgorf.views import PhoneticFormView

from kerofis.views import LocationView
from kerofis.views import LocationCategoryView
from kerofis.views import InformantView
from kerofis.views import KerofisStatView
from kerofis.views import KerofisExportView
from kerofis.views import CityView
from kerofis.views import StandardizedFormView
from kerofis.views import PhoneticTranscriptionView
from kerofis.views import OldFormView
from kerofis.views import OtherFormView
from kerofis.views import AttestedFormView

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
api.register(r'phonetic_form', PhoneticFormView)
api.register(r'locations', LocationView)
api.register(r'location_categories', LocationCategoryView)
api.register(r'informants', InformantView)
api.register(r'stats/kerofis', KerofisStatView)
api.register(r'export/kerofis', KerofisExportView)
api.register(r'cities', CityView)
api.register(r'standardized_forms', StandardizedFormView)
api.register(r'phonetic_transcriptions', PhoneticTranscriptionView)
api.register(r'old_forms', OldFormView)
api.register(r'other_forms', OtherFormView)
api.register(r'attested_forms', AttestedFormView)
api.trailing_slash = '/?'
