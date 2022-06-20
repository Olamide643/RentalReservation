from rest_framework import serializers
from .models import Rental, Reservation


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"
    
            
        
class RentalSerializer(serializers.ModelSerializer):
     class Meta:
         model = Rental
         fields = "__all__"
         
         
         
         
    
        
        
    





