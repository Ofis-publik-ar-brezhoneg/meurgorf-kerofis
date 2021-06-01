from rest_framework import routers

from kerofis.views import LocationView


api = routers.SimpleRouter()
api.register(r'locations', LocationView)
api.trailing_slash = '/?'
