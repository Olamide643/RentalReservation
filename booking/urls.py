from django.urls import path

from .views import RentalAllView, RentalView, ReservationView,ReservationAllView
from.webview import *

urlpatterns = [
    path('api/rentals/', RentalAllView.as_view(), name = "rentals"),
    path('api/rental/<rental_id>/', RentalView.as_view(), name = 'rental'),
    path('api/reservation/<reservation_id>/', ReservationView.as_view(), name ="reservation"),
    path('api/reservations/', ReservationAllView.as_view(), name = "reservations"),
    path('rental/', RentalDisplayView.as_view(), name = 'rental-view'),
    path('rental/<rental_id>/', SingleRentalBookingView.as_view(), name = 'rental-single-view'),
    path('booking/<pk>/',ReservationBookingView.as_view(), name = 'booking' ),
    path('booking/',ReservationBookingView.as_view(), name = 'booking' ),
     path('/', AllRentalBookingView.as_view(), name = 'rentals-view'),
    path('rentals/', AllRentalBookingView.as_view(), name = 'rentals-view'),
    path('bookings/',AllReservationBookingView.as_view(), name = 'bookings' ),
    path('booking/delete/<reservation_id>/<rental_id>',DeleteReservationBookingView.as_view(), name = 'booking-delete' ),
    path('booking/update/<reservation_id>/',UpdateReservationBookingView.as_view(), name = 'booking-update' ),
    path('rental/delete/<rental_id>',DeleteRentalView.as_view(), name = 'rental-delete' ),  
]