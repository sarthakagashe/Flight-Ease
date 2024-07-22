from django.db import models
from datetime import timedelta, timezone
from django.utils import timezone
from django.contrib.auth.models import User
from  django.core.validators import RegexValidator
# Create your models here.

# class User(AbstractUser):
#     def __str__(self):
#         return f"{self.id}: {self.fname} {self.lname}"

class Request(models.Model):
    origin = models.CharField(max_length=64)
    destination = models.CharField(max_length=64)
    date = models.CharField(max_length=64)
    passengers = models.CharField(max_length=64)
    deptime = models.CharField(max_length=64)
    arrtime = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.origin}, {self.destination} ({self.passengers})"

class Flight(models.Model):
    flight_number = models.CharField(max_length=15)
    airlines_name = models.CharField(max_length=20)
    source = models.CharField(max_length=20)
    destination = models.CharField(max_length=20)
    arrival_time = models.DateTimeField(null=True)
    departure_time = models.DateTimeField(null=True)
    fare = models.FloatField(null=True)
    delay = models.DurationField(default= timedelta(hours=1,minutes=30))
    available_seats = models.IntegerField(null=True)
    distance = models.FloatField(default = 300)
     

    
    def _str_(self):
        return f"{self.flight_number} from {self.source} to {self.destination}"
    
    @property
    def estimated_departure_time(self):
        if self.departure_time is not None:
            return self.departure_time + self.delay
        return None
    
    @property
    def estimated_arrival_time(self):
        if self.arrival_time is not None:
            return self.arrival_time + self.delay
        return None
    
    @property
    def distance_left(self):
        curr = timezone.now()
        if self.distance is not None:
            if curr >= self.estimated_departure_time and curr <= self.estimated_arrival_time:
                return (self.distance * (self.estimated_arrival_time - curr))/(self.estimated_arrival_time - self.estimated_departure_time)
            elif curr > self.estimated_arrival_time:
                return 0
            else:
                return self.distance
        else:
            return None 
           
    @property
    def curr_delay(self):
        curr = timezone.now()
        if self.delay is not None:
            if self.departure_time and self.estimated_departure_time:
                if curr >= self.departure_time and curr <= self.estimated_departure_time:
                    remaining_delay = self.delay - (curr - self.departure_time)
                    temp = remaining_delay.total_seconds() / 60  
                    return int(temp)
                elif curr > self.estimated_departure_time:
                    return 0
                else:
                    temp = self.delay.total_seconds() / 60
                    return int(temp)
        return None 


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE)
    booking_time = models.DateTimeField(auto_now_add=True)
    is_canceled = models.BooleanField(default=False)
    req_seats = models.IntegerField(default=1)

    def cancel_ticket(self):
        # Mark the booking as canceled
        self.is_canceled = True
        self.save()


    def __str__(self):
        return f"{self.user.username} - {self.flight.flight_number}"
    
class Passenger(models.Model):
    booking = models.ForeignKey(Booking, related_name='passengers', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    phone_number = models.CharField(max_length=10,validators=[RegexValidator(regex=r'^\d{10}$', message='Phone number must be exactly 10 digits.' ) ])