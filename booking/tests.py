
from django.urls import reverse
from .models import Rental, Reservation
from rest_framework.test import APITestCase
from rest_framework import status


# Create your tests here.
class RentalTests(APITestCase):
    
    
    def test_create_rental(self):
        
        """
        Ensure we can create a new rental object
        """
        url = reverse('rentals')
        
        data = {"name": "Rental A"}
        response = self.client.post(url,data,format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED )
        self.assertEqual(response.data, {"description": "New Rental Successfully Created","data": {"id": 1, "name" :"Rental A" }} )
        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(Rental.objects.get().name, 'Rental A')
        
        
    
        url = reverse('rentals')
        data = {"name": "Rental B"}
        response = self.client.post(url,data,format = 'json')
        self.assertEqual(response.status_code,  status.HTTP_201_CREATED )
        self.assertEqual(response.data, {"description": "New Rental Successfully Created","data": {"id": 2, "name" :"Rental B" }} )
        self.assertEqual(Rental.objects.count(), 2)
    
        
        
    def test_get_all_rental(self):
        """
        Ensure we can fectch all rental object
        """
        url = reverse("rentals") 
        response = self.client.get(url)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(Rental.objects.count(), 1)
        self.assertEqual(len(response.data), 2)

    def test_get_rental(self):
        """
        Ensure we can fectch  rental object with id
        """
        url = reverse("rental",args = [1])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"description": "Rental Record successfully fetched","data": {"id": 1, "name" :" Rental A" }} )

        
    def update_rental(self):
        
        """"
        Ensure we can update a rental object
        """
        url = reverse("rental",args = [1])
        data = {"name": "Rental A+" }
        response = self.client.put(url,data,format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED )
        self.assertEqual(response.data, {"description": "Rental Record Successfully Updated","data": {"id": 1, "name" :" Rental A+" }} )
        
    
    def delete(self):
        
        # Positve Test with a valid rental Id
        url = reverse("rental",args = [1])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data,  {"description": "Succesfully Deleted Rental Details"})
        self.assertEqual(Rental.objects.count(), 1)
        
        
        # Negative Test to delete Invalid rental Id
        url = reverse("rental",args = [9])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status = status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data, {"description": "reservation Id does not exist"})
        
        
        




class ReservationTests(APITestCase): 
    
    def test_create_reservation(self):
        
        """
        Ensure we can create a new reservation object
        """
        url = reverse('reservations')
        data =  {"rental_id": 1, "name": "Reservation 1", "checkin": "2022-06-15T06:12:00Z","checkout": "2022-06-23T12:00:00Z"}
        response = self.client.post(url,data,format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, {"description": "Reservation Successfully Created","data" : {"id": 1,"name": "Reservation 1",
                                         "checkin": "2022-06-15T06:12:00Z","checkout": "2022-06-23T12:00:00Z","previous_reservation": None,"rental_id": 1}} )
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(Reservation.objects.get().name, 'Reservation 1') 
        
        
    
        url = reverse('reservations')
        data =  {"rental_id": 1, "name": "Reservation 2", "checkin": "2022-06-15T06:12:00Z","checkout": "2022-06-23T12:00:00Z"}
        response = self.client.post(url,data,format = 'json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED )
        self.assertEqual(response.data, {"description": "Reservation Successfully Created","data" : {"id": 2,"name": "Reservation 2",
                                         "checkin": "2022-06-15T06:12:00Z","checkout": "2022-06-23T12:00:00Z","previous_reservation": 1,"rental_id": 1}} ) 
        self.assertEqual(Reservation.objects.count(), 2)
        self.assertEqual(Reservation.objects.get().name, 'Reservation 2')
        
        
   
    def test_get_all_reservation(self):
        """
        Ensure we can fectch all reservations 
        """
        url = reverse("reservations")
        response = self.client.post(url,format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Reservation.objects.count(), 1)
        self.assertEqual(len(response.data), 2) 
   
    
    def test_get_reservation(self):
        """
        Ensure we can fectch all reservation with reservation ID
        """
        url = reverse("reservation",args = [2])
        response = self.client.post(url,format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"description" : "Successfully fectched a record for reservation Id", 
                                         "data":{"id": 2,"name": "Reservation 2",
                                         "checkin": "2022-06-15T06:12:00Z",
                                         "checkout": "2022-06-23T12:00:00Z","previous_reservation": 1,"rental_id": 1}})

        
    def update_rental(self):
        
        """"
        Ensure we can update a reservation
        """
        url = reverse("reservation",args = [2])
        data = {"name": "Reservation A+","checkin": "2022-06-16T06:12:00Z",
                                         "checkout": "2022-06-24T12:00:00Z","rental_id": 2 }
        response = self.client.put(url,data,format = 'json')
        self.assertEqual(response.status_code, status.HTTP_200_OK )
        self.assertEqual(response.data.description, "Reservation Successfully Updated" )
        
    
    def delete(self):
        
        """"
        Ensure we can delete a reservation 
        """
        
        # Positve Test with a valid rental Id
        
        url = reverse("reservation",args = [2])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data,  {"description": "Succesfully deleted Reservation"})
        self.assertEqual(Rental.objects.count(), 1)
        
        
        # Negative Test to delete Invalid rental Id
        url = reverse("reservation",args = [9])
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(response.data,  {"detail": "Not found."})
        
        