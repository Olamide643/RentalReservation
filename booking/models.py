from django.db import models
from django.utils import timezone

# Create your models here.

class Rental(models.Model):
    name = models.CharField(max_length=250, unique = True) 
    
    def __str__(self):
        return str(self.name)
    
    
class Reservation(models.Model):
    name = models.CharField(max_length= 250)
    checkin = models.DateTimeField(default=timezone.now)
    checkout = models.DateTimeField()
    rental_id = models.ForeignKey('Rental', related_name= 'rental', on_delete= models.CASCADE)
    previous_reservation = models.IntegerField(null=True)
    
    

    def __str__(self):
        return str(self.id)
