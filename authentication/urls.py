from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
   path('', views.signin, name = "signin"),
   path('signup', views.signup, name = "signup"),
   path('signin', views.signin, name = "signin"),
   path('signout', views.signout, name = "signout"),
   path('book', views.book, name = "book"),
   path('search', views.search, name = "search"),
   path('book-flight/<int:flight_id>/', views.book_flight, name='book_flight'),
   path('booking_history/generate_graph/', views.yearly_graph, name='yearly_graph'),
   path('yearly_graph/', views.generate_graph_html, name='generate_graph_html'),
   # path('flightDetails', views.)

   path('booking_history/', views.booking_history, name = "booking_history"),
   path('cancel_booking/<str:booking_id>/', views.cancel_booking, name='cancel_booking'),
   path('flight_details/<int:flight_id>/', views.flight_details, name = 'flight_details'),
   path('booking_history/generate_chart/', views.generate_pie_chart, name='generate_pie_chart'),

   path('passenger_details/<str:booking_id>/', views.passenger_details, name = 'passenger_details'),
   path('render_details_page/<str:booking_id>/',views.render_details_page, name='render_details_page'),
   
   path('get_chart/', views.generate_chart_html, name='generate_chart_html'),
   path('fetch_filtered_flights/', views.fetch_filtered_flights, name='fetch_filtered_flights'),
    # path('flights-data/', views.get_flights_data, name='flights_data'),
   
   path('get_booking_details/', views.get_booking_details, name='get_booking_details'),
   path('profile/', views.profile_view, name='profile'),
]
