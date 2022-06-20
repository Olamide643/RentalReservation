

from django.shortcuts import  redirect, render
from .forms import RentalForm, ReservationBookingForm, ReservationForm
from  .models import Rental, Reservation
from django.views.generic import View
from django.urls import reverse



# Class Based View to create new rental Object

class RentalDisplayView(View):
    context = {}

    def get(self,request):
        form = RentalForm()
        self.context['form'] = form
        return render(request,'index.html',self.context)

    def post(self,request):
        form = RentalForm(request.POST)
        if form.is_valid():
            saved_form = form.save()
            self.context['form'] = form
            self.context['rental'] = Rental.objects.get(pk =saved_form.id )
            return render(request, 'Rental.html', self.context)
        
        self.context['form'] = form
        return render(request, 'Rental.html', self.context)
    

# Class based view to display all rentals Object

class AllRentalBookingView(View):
    context = {}
    def get(self,request):
        form = RentalForm()
        self.context['form'] = form
        self.context['rentals'] = Rental.objects.all()
        return render(request, 'display.html', self.context)


# Class based view to display a rental object  

class SingleRentalBookingView(View):
    context = {}
    def get(self,request,rental_id):
        form = Rental()
        self.context['form'] = form
        try:
            rental = Rental.objects.get(pk=rental_id)
        except Rental.DoesNotExist:
            return render(request,"404Rentalerror.html")
        self.context['rental'] = rental
        self.context['reservations'] = Reservation.objects.filter(rental_id = rental_id).order_by("-id")
        return render(request, 'singlerental.html', self.context)
    

# Class based view to destroy a rental object
    
class DeleteRentalView(View):
    
    def post(self, request,rental_id):
        rental = Rental.objects.get(pk=rental_id)
        rental.delete()
        return redirect('rentals-view')
    
    

# Class Based View to create new reservation object
  
class ReservationBookingView(View):
    context = {}

    def get(self,request,pk = None):
        form = ReservationBookingForm()
        self.context['form'] = form
        self.context['form'] = form
        return render(request,'reservationcreate.html',self.context)

    def post(self,request):
        form = ReservationBookingForm(request.POST)
        if form.is_valid():
            new_reservation = form.save(commit= False)
            new_reservation.previous_reservation = form.cleaned_data["previous_reservation"]
            new_reservation.save()
        self.context['form'] = form
        self.context['reservation'] = Reservation.objects.get(pk = new_reservation.id )
        return render(request, 'Singlereservation.html', self.context)
    

# Class based view to display all reservations object

class AllReservationBookingView(View):
    context = {}
    def get(self,request):
        form = ReservationBookingForm()
        self.context['form'] = form
        self.context['reservations'] = Reservation.objects.all()
        return render(request, 'reservation.html', self.context)
    
  

    

# Class based view to destroy a reservation object   

class DeleteReservationBookingView(View):
    def post(self, request, reservation_id,rental_id):
        try:
            reservation = Reservation.objects.get(pk=reservation_id)
        except Reservation.DoesNotExist:
            return render(request,"404error.html")
        reservation = Reservation.objects.get(pk=reservation_id)
        reservation.delete()
        return redirect('bookings')
    

# Class based view to update a reservation 

class UpdateReservationBookingView(View):
    context = {}
    def get(self, request,reservation_id):
        
        try:
            reservation = Reservation.objects.get(pk=reservation_id)
        except Reservation.DoesNotExist:
            return render(request,"404error.html")
        form = ReservationForm(instance=reservation) 
        print(form.data)
        self.context['form'] = form
        return  render(request, 'updatereservation.html', self.context)
        
    
    
    def post(self, request, reservation_id):
        try:
            reservation = Reservation.objects.get(pk=reservation_id)
        except Reservation.DoesNotExist:
            return render(request,"404error.html")
        form = ReservationForm(request.POST)
        reservation.name = form.data["name"]
        reservation.checkout = form.data["checkout"]
        reservation.checkin = form.data["checkin"]
        if reservation.rental_id != form.data["rental_id"]:
            last_reservation = Reservation.objects.filter(rental_id = form.data["rental_id"]).order_by('-id')
            if last_reservation.exists():
                prev_reservation =  last_reservation[0].id
            else:
                prev_reservation = None
            reservation.previous_reservation = prev_reservation 
    
        reservation.rental_id  = Rental.objects.get(pk=form.data["rental_id"])
        reservation.save()
        return redirect('bookings')
    


        
    
        
