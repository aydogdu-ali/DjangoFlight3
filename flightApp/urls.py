from django.urls import path, include

from rest_framework import routers #Modelvieset kullandığımız için  routers import ediyoruz.

from.views import FlightView #views import ediyoruz.

from.views import ReservationView #views ten import ediyoruz.

router = routers.DefaultRouter()
router.register('flights',FlightView )
router.register("reservations", ReservationView)

urlpatterns = [
   
]
urlpatterns += router.urls