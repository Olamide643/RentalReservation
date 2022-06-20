from django.shortcuts import get_object_or_404
from .serializer import RentalSerializer, ReservationSerializer 
from  rest_framework.response import Response
from .models import Rental, Reservation
from rest_framework import status
from rest_framework.views import APIView



# Create your views here.


# Class Based view to fetch all rentals and create a rental object
class RentalAllView(APIView):
    
    def get(self, request):
        queryset = Rental.objects.all()
        
        if queryset.exists():
            serializer = RentalSerializer(queryset,many=True)
            
            response ={"description": "Rental Records Found","data": serializer.data}
            return Response(response,status = status.HTTP_200_OK)
        
        response = {'description': "No  Rental Record Found","data": None}
        return Response(response,status = status.HTTP_204_NO_CONTENT)
        
    
    def post(self,request):
        serialized_data = RentalSerializer(data = request.data)
        
        if serialized_data.is_valid():
            
            serialized_data.save()
            message = {"description": "New Rental Successfully Created","data" : serialized_data.data}
            return Response(message, status = status.HTTP_201_CREATED)  
         
        return Response(serialized_data.error)
        
   

# Class Based view to fetch, update and delete a rental object
 
class RentalView(APIView):
    def get_object(self, rental_id):
        rental = get_object_or_404(Rental,pk =rental_id)
        return rental
           
    def get(self,request,rental_id):
        try:
            rental = Rental.objects.get( pk = rental_id)
        except:
            message = {"description": "Rental Id does not exist"}
            return Response(message, status = status.HTTP_404_NOT_FOUND)
        serialized_data = RentalSerializer(rental)
        message = {"description": "Rental Record successfully fetched","data": serialized_data.data}
        return Response(message, status = status.HTTP_200_OK)
            
        
    def put(self,request,rental_id):
        try:
            rental = Rental.objects.get( pk = rental_id)
        except:
            message = {"description": "Rental Id does not exist"}
            return Response(message, status = status.HTTP_404_NOT_FOUND)
        request_name = request.data.get("name", None)
        
        if request_name:
            rental_name = Rental.objects.filter(name = request_name).first()
            if rental_name:
                
                message = {"description": "Rental Name already exist","error": "Name already exist"}
                return Response(message, status = status.HTTP_400_BAD_REQUEST)
            
        serialized_request = RentalSerializer(instance = rental, data = request.data, partial= True)
        
        if serialized_request.is_valid():
            try:
                serialized_request.save()
                message = {"description": "Rental Record Successfully Updated","data": serialized_request.data}
                return Response(message, status =status.HTTP_200_OK)
            
            except Exception as e :
                message = {"description": "An error occurred while updating the Rental details", "error": e.message}
                return Response(message, status =status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:  
            message = {"description" : "Rental Update Unsuccessful","error": serialized_request.error}
            return Response(message, status = status.HTPP_400_BAD_REQUEST)
        
    def delete(self, request,rental_id):
        try:
            rental = Rental.objects.get( pk = rental_id)
        except:
            message = {"description": "Rental Id does not exist"}
            return Response(message, status = status.HTTP_404_NOT_FOUND)
        try:
            rental.delete()
            message = {"description": "Succesfully Deleted Rental Details"}
            return Response(message, status = status.HTTP_204_NO_CONTENT)
        except:
            message = {"description": "Unable to delete Rental Id"}
            return Response(message, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
        

# Class Based view to fetch all reservations and create a reservation object

class ReservationAllView(APIView):
    def get(self, request):
        queryset = Reservation.objects.all()
        
        if queryset.exists():
            serializer = ReservationSerializer(queryset,many=True)
            
            response ={"description": "Records found","data": serializer.data}
            return Response(response,status = status.HTTP_200_OK)
        
        response = {'message': "No record found","data": None}
        return Response(response,status = status.HTTP_204_NO_CONTENT)
        
    
    def post(self,request):
        
        rental_id = request.data.get("rental_id",None)
        if not rental_id:
            message = {"description" : "Insertion Failuer"}  
            return Response(message, status =  status.HTTP_400_BAD_REQUEST)
        try:
           rental  =  Rental.objects.get(pk = rental_id)
           
        except Rental.DoesNotExist:
            message = {"description": "Rental Id does not exist"}
            return Response(message, status = status.HTTP_404_NOT_FOUND)
        
        last_reservation = Reservation.objects.filter(rental_id = rental_id).order_by('-id')
        if last_reservation.exists():
            prev_restriction =  last_reservation[0].id
        else:
            prev_restriction = None
        
        
        request.data["previous_reservation"] = prev_restriction

        serialize_request = ReservationSerializer(data = request.data)
        if serialize_request.is_valid():
            serialize_request.save()
            message = {"description": "Reservation Successfully Created","data" : serialize_request.data}
            return Response(message, status = status.HTTP_200_OK) 
        message = {"description" : "Insertion Failuer","error": serialize_request.errors}  
        return Response(message, status =  status.HTTP_400_BAD_REQUEST)


        
        
          
# Class Based view to fetch, update and delete a reservation object object

class ReservationView(APIView):
    
    def get_object(self,reservation_id):
        reservation = get_object_or_404(Reservation,pk =reservation_id)
        return reservation
             
    
    def get(self,request,reservation_id):
        try:
            reservation = Reservation.objects.get( pk = reservation_id)
        except:
            message = {"description": "reservation Id does not exist"}
            return Response(message, status = status.HTTP_404_NOT_FOUND)
        serialized_data = ReservationSerializer(reservation)
        message = {"description" : "Successfully fectched a record for reservation Id", "data": serialized_data.data}
        return Response(message, status = status.HTTP_200_OK)
    
    
    def delete(self,request,reservation_id):
        try:
            reservation = Reservation.objects.get( pk = reservation_id)
        except:
            message = {"description": "reservation Id does not exist"}
            return Response(message, status = status.HTTP_404_NOT_FOUND)
        try:
            reservation.delete()
            message = {"description": "Succesfully deleted Reservation"}
            return Response(message, status = status.HTTP_204_NO_CONTENT)
        except:
            message = {"description": "Unable to delete Reservation"}
            return Response(message, status = status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        
    def put(self,request,reservation_id):
        
        try:
            reservation = Reservation.objects.get( pk = reservation_id)
        except:
            message = {"description": "reservation Id does not exist"}
            return Response(message, status = status.HTTP_404_NOT_FOUND)

        rental_id = request.data.get("rental_id",None)
        
        
        # A sub action to update previous reservation of a reservation object when rental is updated
        if rental_id:
            request.data.pop("previous_reservation")
            try:
                rental  =  Rental.objects.get(pk = rental_id)
            except Rental.DoesNotExist:
                message = {"description": "Rental Id does not exist"}
                return Response(message, status = status.HTTP_404_NOT_FOUND)
        
            last_reservation = Reservation.objects.filter(rental_id = rental_id).order_by('-id')
        
            if last_reservation.exists():
                prev_reservation =  last_reservation[0].id
            else:
                prev_reservation = None
            request.data["previous_reservation"] = prev_reservation
        
        
        serialize = ReservationSerializer(instance = reservation, data = request.data, partial= True)
        if serialize.is_valid():
            try:
                serialize.save()
                message = {"description": "Reservation Successfully Updated","data": serialize.data}
                return Response(message, status =status.HTTP_200_OK)
            except Exception as e :
                message = {"description": "An error occurred while updating Reservation"}
                return Response(message, status =status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        else:
            message = {"description" : "Reservation Update Unsuccessful","error": serialize.error}
            return Response(message, status = status.HTPP_400_BAD_REQUEST)
            
        

    
    
    

        
        
         
        
        
        
        
        
        
            
        
