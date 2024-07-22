from os import environ
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse
from authentication.models import Request
from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import ExtractMonth
import calendar

from django.http import JsonResponse
from .models import Booking, Passenger


from authentication.models import Flight,Booking
from datetime import datetime, timedelta
import random
from django.db.models import Q

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages

def profile_view(request):
    if request.user.is_authenticated:  
        user = request.user
        if request.method == 'POST':
            username = request.POST.get('username')
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            email = request.POST.get('email')
            
            if username:
                user.username = username
            if first_name:
                user.first_name = first_name
            if last_name:
                user.last_name = last_name
            if email:
                user.email = email
            
            user.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('signin')
        
        return render(request, 'authentication/profile.html', {'user': user})
    else:
        return redirect('signin')

def signup(request):

    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensuring password matches confirmation
        password = request.POST["pass1"]
        confirmation = request.POST["pass2"]
        if password != confirmation:
            return render(request, "authentication/signup.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.first_name = fname
            user.last_name = lname
            user.save()
        except:
            return render(request, "authentication/signup.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return redirect('book')

    else:
        return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["pass1"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('book')

            
        else:
            return render(request, "authentication/signin.html", {
                "message": "Invalid username and/or password."
            })
    else:
        if request.user.is_authenticated:
            return redirect('book')

        else:
            return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse("signin"))

def book(request):
     if request.user.is_authenticated:
        return render(request, "authentication/temp.html")
     else:
         return redirect('signin')

    
def search(request):
    if request.user.is_authenticated:
        current_datetime = timezone.now()

        total_flights = len(Flight.objects.all())

        slotMatch = {}
        slotMatch["morning"] = (6,12)
        slotMatch["afternoon"] = (12,18)
        slotMatch["evening"] = (18,24)
        slotMatch["night"] = (0,6)
        # Parse user query parameters
        if request.method == "POST":
            print(request)

            origin = request.POST['source']
            destination = request.POST['destination']
            date = datetime.strptime(request.POST['journeyDate'], '%Y-%m-%d').date()
            passengers = int(request.POST['counter'])
            depSlot = request.POST['departureTime']
            arrSlot = request.POST['arrivaltime']
            print(depSlot)
            print(arrSlot)

            request.session['search_params'] = {
                'origin': origin,
                'destination': destination,
                'date': str(date),
                'passengers': passengers,
                'depSlot': depSlot,
                'arrSlot': arrSlot,
            }

            if depSlot!= "no" :
                depStart = slotMatch[depSlot][0]
                depEnd = slotMatch[depSlot][1]
            if arrSlot !="no":
                arrStart = slotMatch[arrSlot][0]
                arrEnd = slotMatch[arrSlot][1]
        
            
            # Step 1: Query flights based on user search criteria
            flights_old = Flight.objects.filter(
                source=origin,
                destination=destination,
                # estimated_departure_time__date=date,
            )
            flights_old = flights_old.filter(available_seats__gte = passengers)
    
            flights = []
            
            for flight in flights_old:
                
                if (flight.estimated_departure_time + timedelta(hours=5.5)).date() == date and flight.estimated_departure_time > current_datetime:
                    print("est dpt")
                    print(flight.estimated_departure_time)
                    flights.append(flight)
            curavail = len(flights)
            
            flights_ad =[]
            flights_d =[]
            flights_a =[]
            x =  timedelta(hours =5.5)
            if depSlot != "no" and arrSlot != "no":

                for flight in flights:
                    # print("est dpt")
                    # print(flight.estimated_departure_time)
                    # print("&&&&&&&&&&&SBDSJSJs")
                    # print(flight.delay)
                    # print(flight.departure_time)
                    # print(flight.estimated_departure_time)
                    # print(flight.estimated_arrival_time)
                    # 
                    # print(flight.departure_time)
                    # flight.departure_time = flight.departure_time - timedelta(hours =5.5)
                    # flight.arrival_time = flight.arrival_time - timedelta(hours =5.5)
                    # print((flight.estimated_departure_time + timedelta(hours=5.5)).time().hour)
                    # print((flight.arrival_time + timedelta(hours=5.5)).time().hour)
                    if (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour  >= depStart and (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour < depEnd and  (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour >= arrStart and (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour < arrEnd:
                        flights_ad.append(flight)
                    elif (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour  >= depStart and (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour < depEnd :
                        flights_d.append(flight)
                    elif (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour  >= arrStart and (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour < arrEnd:
                        flights_a.append(flight)

            elif depSlot != "no":
                for flight in flights:
                    if (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour  >= depStart and (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour < depEnd : 
                        flights_d.append(flight)
            elif arrSlot != "no":
                for flight in flights:

                # print("dsddsdkjkjjjjjjjjjjjj")
                    if (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour  >= arrStart and (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour < arrEnd:
                        flights_a.append(flight)


            answer_array = []
            if len(flights_ad) != 0:
                print("AD")
                answer_array = flights_ad
            elif len(flights_d) != 0:
                print("D")
                answer_array = flights_d
            elif len(flights_a) != 0:
                print("A")
                answer_array = flights_a
            else :
                print("flights")
                answer_array = flights  
            
            # print("FLight AD")  
            # print(flights_ad)
            # print("FLight D")
            # print(flights_d)
            # print("FLight A")
            # print(flights_a)
            answer_array = sorted(answer_array, key=lambda Flight: Flight.delay)
            curavail = len(answer_array)
            flights_data = []
            for flight in answer_array:
                delay_in_minutes = flight.delay.total_seconds() / 60 if flight.delay else 0
                delay_in_minutes_int = int(delay_in_minutes)
                
                flights_data.append({
                    'flight_number': flight.flight_number,
                    'airlines_name': flight.airlines_name,
                    'source': flight.source,
                    'destination': flight.destination,
                    'departure_time': flight.departure_time,
                    'arrival_time': flight.arrival_time,
                    'fare': flight.fare,
                    'available_seats': flight.available_seats,
                    'flight_id': flight.id,
                    'delay': flight.curr_delay,
                    'estimated_departure_time': flight.estimated_departure_time,
                    'estimated_arrival_time': flight.estimated_arrival_time,
                    'distance': flight.distance
                })
            return render(request, 'authentication/flight_list.html', {'flights': flights_data, 'curavail': curavail, 'totavail': total_flights})
    else:
            return redirect('signin')
            
def flight_details(request, flight_id):
    if request.user.is_authenticated:
        flight = Flight.objects.get(pk=flight_id)
        delay_in_minutes = flight.delay.total_seconds() / 60 if flight.delay else 0
        delay_in_minutes = int(delay_in_minutes)
        flight_data = {
            'flight_number': flight.flight_number,
            'airlines_name': flight.airlines_name,
            'source': flight.source,
            'destination': flight.destination,
            'departure_time': flight.departure_time,
            'arrival_time': flight.arrival_time,
            'fare': flight.fare,
            'available_seats': flight.available_seats,
            'flight_id': flight_id,
            'delay': flight.curr_delay,
            'estimated_departure_time' : flight.estimated_departure_time,
            'estimated_arrival_time' : flight.estimated_arrival_time,
        }
        return render(request, 'authentication/passenger.html', {'flight': flight_data})
    else:
        return redirect('signin')


def book_flight(request, flight_id):
    if request.user.is_authenticated:
        flight = Flight.objects.get(pk=flight_id)
        timenow = datetime.now()
 
        print(request)
        print(dict(request.POST))
        # Get the number of passengers from the POST request
        num_passengers = int(request.POST.get('num_passengers', 0))
        print(num_passengers)
        # passengers =  request.POST['passengers']
        # print(passengers)
        if num_passengers <= flight.available_seats:
            flight.available_seats -= num_passengers
            flight.save()
 
            # Create the booking
            booking = Booking.objects.create(flight=flight, user=request.user, booking_time=timenow, req_seats=num_passengers)
 
            # Retrieve and save passenger details
            for i in range(num_passengers):                
                Passenger.objects.create(
                    booking=booking,
                    first_name=request.POST.get(f'passengers[{i}][first_name]'),
                    last_name=request.POST.get(f'passengers[{i}][last_name]'),
                    age=int(request.POST.get(f'passengers[{i}][age]')),
                    gender=request.POST.get(f'passengers[{i}][gender]'),
                    phone_number=request.POST.get(f'passengers[{i}][phone_number]')
                )
 
            messages.success(request, 'Flight booked successfully!')
            return JsonResponse({'redirect_url': reverse('booking_history')})
        else:
            messages.error(request, 'Not enough available seats for this booking.')
            return JsonResponse({'redirect_url': reverse('book')})
    else:
        return JsonResponse({'redirect_url': reverse('signin')})
    

 
def booking_history(request):
    # Get bookings associated with the current user
    if request.user.is_authenticated:

        user_bookings = Booking.objects.filter(user=request.user)
    
        # Create a list to store booking details
        booking_details = []
        now = timezone.now()
        for booking in user_bookings:
            iscancelled = booking.is_canceled
            passengers = booking.req_seats
            # print(passengers)
            # Retrieve details from the associated Flight model
            if iscancelled :
                status = "Cancelled"
            else:
                 if booking.flight.estimated_departure_time > now:
                    status = "Pending"
                 else:
                    status = "Completed"
            flight_details = {
                'flight_number': booking.flight.flight_number,
                'airlines_name': booking.flight.airlines_name,
                'source': booking.flight.source,
                'destination': booking.flight.destination,
                'arrival_time': booking.flight.arrival_time,
                'departure_time': booking.flight.departure_time,
                'fare': booking.flight.fare,
                'delay': booking.flight.curr_delay,
                'booking_time': booking.booking_time,
                'booking_id': booking.id,
                'status' : status,
                'passengers' : passengers,
                
            }

            # print(booking.flight.flight_number)
            # Append flight details to the list
            # if not iscancelled: 
            booking_details.append(flight_details)
        booking_details.reverse()
        return render(request, 'authentication/booking_history.html', {'booking_details': booking_details})
    else:
        return redirect('signin')

def cancel_booking(request, booking_id):
    if request.user.is_authenticated:

        booking = Booking.objects.get(id=booking_id)
        # print(booking_id)
        # Cancel the ticket
        booking.cancel_ticket()
        flight = Flight.objects.get(pk=booking.flight_id)
        currSeats = flight.available_seats
        seats_cancelled = booking.req_seats
        # print(currSeats)
        # print(seats_cancelled)
        # print(flight)
        flight.available_seats += seats_cancelled
        flight.save()
        return redirect('booking_history')
    else:
        return redirect('signin')
    
def get_booking_details(request):
    
    # Get bookings associated with the current user
    if request.user.is_authenticated:

        user_bookings = Booking.objects.filter(user=request.user)
    
        # Create a list to store booking details
        booking_details = []
        now = timezone.now()
        for booking in user_bookings:
            iscancelled = booking.is_canceled
            passengers = booking.req_seats
            # print(passengers)
            # Retrieve details from the associated Flight model
            if iscancelled :
                status = "Cancelled"
            else:
                 if booking.flight.estimated_departure_time > now:
                    status = "Pending"
                 elif booking.flight.estimated_departure_time < now and booking.flight.estimated_arrival_time > now:
                    status = "In-Transit"
                 else:
                    status = "Completed"
            curr_delay = booking.flight.delay.total_seconds()/60
            delay_in_minutes = int(curr_delay)
            travel_time = booking.flight.arrival_time - booking.flight.departure_time

            travel_distance = int(booking.flight.distance_left)
            
            flight_details = {
                'flight_number': booking.flight.flight_number,
                'airlines_name': booking.flight.airlines_name,
                'source': booking.flight.source,
                'destination': booking.flight.destination,
                'arrival_date': booking.flight.arrival_time,
                'arrival_time': booking.flight.arrival_time,
                'departure_date': booking.flight.departure_time,
                'departure_time': booking.flight.departure_time,
                'fare': booking.flight.fare,
                'delay': booking.flight.curr_delay,
                'booking_time': booking.booking_time,
                'booking_id': booking.id,
                'status' : status,
                'passengers' : passengers,
                'estimated_departure_time' : booking.flight.estimated_departure_time,
                'estimated_departure_date' : booking.flight.estimated_departure_time,
                'estimated_arrival_time' : booking.flight.estimated_arrival_time,
                'estimated_arrival_date' : booking.flight.estimated_arrival_time,
                'distance_left' : travel_distance,
            }

            # Append flight details to the list
            # if not iscancelled: 
            booking_details.append(flight_details)

        booking_details.reverse()            
        
        return JsonResponse(booking_details, safe=False)
    
    else:
        return redirect('signin')



def fetch_filtered_flights(request):
    if request.user.is_authenticated:
        current_datetime = timezone.now()

        total_flights = len(Flight.objects.all())

        slotMatch = {}
        slotMatch["morning"] = (6,12)
        slotMatch["afternoon"] = (12,18)
        slotMatch["evening"] = (18,24)
        slotMatch["night"] = (0,6)
        # if 'search_params' in request.session:
        #     search_params = request.session['search_params']
        search_params = request.session['search_params']
        if search_params:
            origin = search_params['origin']
            destination = search_params['destination']
            date = datetime.strptime(search_params['date'], '%Y-%m-%d').date()
            passengers = search_params['passengers']
            depSlot = search_params['depSlot']
            arrSlot = search_params['arrSlot']

            if depSlot!= "no" :
                depStart = slotMatch[depSlot][0]
                depEnd = slotMatch[depSlot][1]
            if arrSlot !="no":
                arrStart = slotMatch[arrSlot][0]
                arrEnd = slotMatch[arrSlot][1]
        
            
            # Step 1: Query flights based on user search criteria
            flights_old = Flight.objects.filter(
                source=origin,
                destination=destination,
                # estimated_departure_time__date=date,
            )
            flights_old = flights_old.filter(available_seats__gte = passengers)

            flights = []
            
            for flight in flights_old:
                
                if (flight.estimated_departure_time + timedelta(hours=5.5)).date() == date and flight.estimated_departure_time > current_datetime:
                    # print("est dpt")
                    # print(flight.estimated_departure_time)
                    flights.append(flight)
            curavail = len(flights)
            
            # print(current_datetime)
            flights_ad =[]
            flights_d =[]
            flights_a =[]
            x =  timedelta(hours =5.5)
            if depSlot != "no" and arrSlot != "no":

                for flight in flights:
                    # print("est dpt")
                    # print(flight.estimated_departure_time)
                    # print("&&&&&&&&&&&SBDSJSJs")
                    # print(flight.delay)
                    # print(flight.departure_time)
                    # print(flight.estimated_departure_time)
                    # print(flight.estimated_arrival_time)
                    # 
                    # print(flight.departure_time)
                    # flight.departure_time = flight.departure_time - timedelta(hours =5.5)
                    # flight.arrival_time = flight.arrival_time - timedelta(hours =5.5)
                    # print((flight.estimated_departure_time + timedelta(hours=5.5)).time().hour)
                    # print((flight.arrival_time + timedelta(hours=5.5)).time().hour)
                    if (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour  >= depStart and (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour < depEnd and  (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour >= arrStart and (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour < arrEnd:
                        flights_ad.append(flight)
                    elif (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour  >= depStart and (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour < depEnd :
                        flights_d.append(flight)
                    elif (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour  >= arrStart and (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour < arrEnd:
                        flights_a.append(flight)

            elif depSlot != "no":
                for flight in flights:
                    if (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour  >= depStart and (flight.estimated_departure_time + timedelta(hours=5.5)).time().hour < depEnd : 
                        flights_d.append(flight)
            elif arrSlot != "no":
                for flight in flights:
                    # print("dsddsdkjkjjjjjjjjjjjj")
                    if (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour  >= arrStart and (flight.estimated_arrival_time + timedelta(hours=5.5)).time().hour < arrEnd:
                        flights_a.append(flight)
            
            answer_array = []
            if len(flights_ad) != 0:
                print("AD")
                answer_array = flights_ad
            elif len(flights_d) != 0:
                print("D")
                answer_array = flights_d
            elif len(flights_a) != 0:
                print("A")
                answer_array = flights_a
            else :
                print("flights")
                answer_array = flights  
            
            # print("FLight AD")  
            # print(flights_ad)
            # print("FLight D")
            # print(flights_d)
            # print("FLight A")
            # print(flights_a)
            
            answer_array = sorted(answer_array, key=lambda Flight: Flight.delay)
            curavail = len(answer_array)
            flights_data = []
            for flight in answer_array:
                delay_in_minutes = flight.delay.total_seconds() / 60 if flight.delay else 0
                delay_in_minutes_int = int(delay_in_minutes)
                est_dept_time = (flight.estimated_departure_time + timedelta(hours=5.5)).hour * 60 + (flight.estimated_departure_time + timedelta(hours=5.5)).minute
                est_arr_time = (flight.estimated_arrival_time + timedelta(hours=5.5)).hour * 60 + (flight.estimated_arrival_time + timedelta(hours=5.5)).minute
                # print("dsfdsfd")
                # print(est_arr_time)
                # print(est_dept_time)
                flights_data.append({
                    'flight_number': flight.flight_number,
                    'airlines_name': flight.airlines_name,
                    'source': flight.source,
                    'destination': flight.destination,
                    'departure_time': flight.departure_time,
                    'arrival_time': flight.arrival_time,
                    'fare': flight.fare,
                    'available_seats': flight.available_seats,
                    'flight_id': flight.id,
                    'delay': flight.curr_delay,
                    'estimated_departure_date': flight.estimated_departure_time.date().isoformat(),
                    'estimated_arrival_date' : flight.estimated_arrival_time.date().isoformat(),
                    'estimated_departure_time': int(est_dept_time),
                    'estimated_arrival_time': int(est_arr_time),
                    'distance' : flight.distance
                })
            
            
            return JsonResponse(flights_data, safe =False)
    else:
        return redirect('signin') 


def generate_chart_html(request):
    if request.user.is_authenticated:
        return render(request, 'authentication/chart.html')
    else:
        return redirect('signin')
   
 
def generate_pie_chart(request):
    # Fetch the most recent 20 bookings
    if request.user.is_authenticated:
 
        user_bookings = Booking.objects.filter(user=request.user)
        recent_bookings = user_bookings.order_by('-booking_time')[:30]
       
        # Initialize a dictionary to store airline counts
        airline_counts = {}
       
        # Count the number of bookings for each airline
        for booking in recent_bookings:
            # Retrieve the flight associated with the booking
            flight = booking.flight
            # Retrieve the airline name from the flight
            airline_name = flight.airlines_name
           
            # If the airline_name is already in the dictionary, increment the count
            if airline_name in airline_counts:
                airline_counts[airline_name] += 1
            else:
                airline_counts[airline_name] = 1
       
        # Prepare data for the pie chart
        data = [{'airline': airline_name, 'count': count} for airline_name, count in airline_counts.items()]
 
        # Return JSON response for Kendo UI Chart
        return JsonResponse(data, safe=False)
   
    else:
        redirect('signin')

def generate_graph_html(request):
    if request.user.is_authenticated:
        return render(request, 'authentication/graph.html')
    else:
        return redirect('signin')
 
def yearly_graph(request):
    if request.user.is_authenticated:
        user_bookings = Booking.objects.filter(user=request.user)
        current_time = timezone.now()
 
        completed_counts = []
        canceled_counts = []
        upcoming_counts = []
        in_transit_counts = []
 
        for booking in user_bookings:
            flight = booking.flight
            estimated_departure = flight.estimated_departure_time
            estimated_arrival = flight.estimated_arrival_time
 
            if not estimated_departure or not estimated_arrival:
                continue
 
            month = estimated_departure.month
 
            if booking.is_canceled:
                canceled_counts.append(month)
            elif estimated_departure > current_time:
                upcoming_counts.append(month)
            elif estimated_arrival < current_time:
                completed_counts.append(month)
            elif estimated_departure <= current_time <= estimated_arrival:
                in_transit_counts.append(month)
 
        # Function to count occurrences per month
        def count_per_month(data):
            counts = {month: 0 for month in range(1, 13)}
            for month in data:
                counts[month] += 1
            return [{'month': month, 'count': count} for month, count in counts.items()]
 
        data = {
            'completed': count_per_month(completed_counts),
            'canceled': count_per_month(canceled_counts),
            'upcoming': count_per_month(upcoming_counts),
            'in_transit': count_per_month(in_transit_counts)
        }
 
        return JsonResponse(data, safe=False)
    else:
        return redirect('signin')
    

def render_details_page(request, booking_id):
    if request.user.is_authenticated:
        return render(request, 'authentication/details.html', {'booking_id' : booking_id})
    else:
        return redirect('signin')


def passenger_details(request,booking_id):
    if request.user.is_authenticated:

        try:
            booking = Booking.objects.get(id=booking_id)
            passengers = booking.passengers.all()
            passenger_list = [{
                'first_name': passenger.first_name,
                'last_name': passenger.last_name,
                'age': passenger.age,
                'gender': passenger.gender,
                'phone_number': passenger.phone_number,
            } for passenger in passengers]
            return JsonResponse(passenger_list, safe=False)
        except Booking.DoesNotExist:
            return JsonResponse({'error': 'Booking not found'}, status=404)
    else:
        return redirect('signin')