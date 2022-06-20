from django import forms
from .models import Rental, Reservation

class ReservationBookingForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data =super(ReservationBookingForm,self).clean()
        
        # A sub process to set attribute previous reservations on the cleaned data
        
        last_reservation = Reservation.objects.filter(rental_id = cleaned_data['rental_id']).order_by('-id')
        
        if last_reservation.exists():
            prev_reservation =  last_reservation[0].id
        else:
            prev_reservation = None
        cleaned_data["previous_reservation"] = prev_reservation
            
            
    class Meta:
        model = Reservation
        fields = "__all__"
        exclude = ['previous_reservation']
        widgets = {
            'name': forms.TextInput(attrs ={"class":"form-control mb-3"} ),
            'rental_id': forms.Select(attrs ={"class":"form-control mb-3"} ),
            'checkin' : forms.DateTimeInput(attrs={'type':'datetime-local', "class":"form-control mb-3"}),
            'checkout' : forms.DateTimeInput(attrs={'type':'datetime-local', "class":"form-control mb-3"})
        }

class ReservationForm(forms.ModelForm):
    
    def clean(self):
        cleaned_data =super(ReservationForm,self).clean()
       
        
        # A sub process to set attribute previous reservations on the cleaned data
        
        last_reservation = Reservation.objects.filter(rental_id = cleaned_data['rental_id']).order_by('-id')
        
        if last_reservation.exists():
            prev_reservation =  last_reservation[0].id
        else:
            prev_reservation = None
        cleaned_data["previous_reservation"] = prev_reservation
    
    
    class Meta:
        model = Reservation
        fields ="__all__"
        widgets ={
                    'name': forms.TextInput(attrs ={"class":"form-control mb-3"} ),
                    'rental_id': forms.Select(attrs ={"class":"form-control mb-3"} ),
                    'checkin' : forms.DateTimeInput(attrs={'type':'datetime-local', "class":"form-control mb-3"}),
                    'checkout' : forms.DateTimeInput(attrs={'type':'datetime-local', "class":"form-control mb-3"})
                 }    
            
        
        
        
class RentalForm(forms.ModelForm):
    class Meta:
        model = Rental
        fields = "__all__"
        widgets = {
                   'name': forms.TextInput(attrs ={"class":"form-control mb-3"} )
                  }
    
    