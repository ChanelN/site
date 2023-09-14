from django.shortcuts import render

from .models import Item, User
from .managers import ItemManager
from bids.models import Bid
from . import serializers
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework import views, permissions, generics
from django.middleware.csrf import get_token
from rest_framework.authentication import SessionAuthentication
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.sessions.models import Session
from django.utils import timezone

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect

class ItemViewSet(ModelViewSet):
    #allow any users to view current items
    #only when bidding or asking questions do they need account
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer
    authentication_classes = []
    permission_classes = []

class AddItem(generics.CreateAPIView):
    queryset = Item.objects.active_items()
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated] #only authenticated users

    def post(self, request, format=None):
        session_id = request.META.get('HTTP_X_SESSIONID')

        # Retrieve the session associated with the provided session ID
        try:
            session = Session.objects.get(session_key=session_id)
        except Session.DoesNotExist:
            return Response({'message': 'Invalid session ID'}, status=status.HTTP_401_UNAUTHORIZED)
        
        # Check if the session is still valid
        if session.expire_date < timezone.now():
            return Response({'message': 'Expired session ID'}, status=status.HTTP_401_UNAUTHORIZED)

        #extract the creator field to set it
        creator = self.request.data.get('creator')
        try:
            creator = User.objects.get(id=creator)   #try find the user
        except User.DoesNotExist:
            return Response({'message': 'Invalid creator id'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = serializers.ItemSerializer(data=request.data)
        if(serializer.is_valid()): 
            item = serializer.save(creator=creator) #automatically handles creation
            return Response({'message': 'Item created', 'item_id': item.id}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ViewUserItems(generics.RetrieveAPIView):
    #this is for GET in sellingOverview = path"auctionItems"
    queryset = Item.objects.active_items()
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]

    #how do i get only items for the specific user - if i send user id
    def get(self, request):
        try:
            user = self.request.user #gets the currently logged in user
            items = Item.objects.active_items().filter(creator=user) #only return items made by this specific user
            serializer = serializers.ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ViewBidderItems(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

    def get(self, request, *args, **kwargs):
        try:
            items = Item.objects.all().filter(winner_id=self.kwargs['id'])
            serializer = serializers.ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# django.core.mail.BadHeaderError
def mailfunction(request):
    if request.method == "POST":
        subject = request.POST.get('subject', '')
        message = request.POST.get('message', '')
        from_email = request.POST.get('from_email', '')
        recipient = request.POST.get('to_email', '')
        #['admin@example.com']
        if subject and message and from_email and recipient:
            try:
                send_mail(subject=subject, message=message, from_email=from_email, recipient_list=[recipient])
            except BadHeaderError as b:
                #return Response({'error': BadHeaderError}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                #return HttpResponse('Invalid header found.')
                return JsonResponse({'error': str(b)}, status=400)
            return JsonResponse({'message' : 'email sent successfully'})
        else:
            #return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            #return HttpResponse('Make sure fields are correct.')
            return JsonResponse({'error': 'Make sure all fields are there'}, status=500)
        
class ViewExpiredItems(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            user = self.request.user
            now = timezone.now()
            items = Item.objects.all().filter(
                creator=user,
                end_time__lt=now,
                is_sold=False
            ).order_by('-end_time')
            serializer = serializers.ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ViewSoldItems(generics.RetrieveAPIView):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            user = self.request.user
            now = timezone.now()
            items = Item.objects.all().filter(
                creator=user,
                end_time__lt=now,
                is_sold=True
            ).order_by('-end_time')
            serializer = serializers.ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class ViewActiveItems(generics.RetrieveAPIView):
    #this is to return only active items in itemList - different from viewUserItems as we don't account for user
    queryset = Item.objects.active_items()
    serializer_class = serializers.ItemSerializer
    permission_classes = [AllowAny]

    def get(self, request):
        try:
            items = Item.objects.active_items()
            serializer = serializers.ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateItem(generics.UpdateAPIView):
    #set creator before saving
    queryset = Item.objects.active_items()
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id' #id of the item

    def put(self,request, *args, **kwargs):
        item = self.get_object()
        if item.is_sold:  # Check if the item is already sold
            return Response({'message': 'Cannot update sold items'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = serializers.ItemSerializer(instance=item, data = self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if 'picture' in request.FILES:
            item.picture = request.FILES['picture']

        creator = self.request.data.get('creator')
        try:
            creator = User.objects.get(id=creator)   #try find the user
        except User.DoesNotExist:
            return Response({'message': 'Invalid creator id'}, status=status.HTTP_400_BAD_REQUEST)
        
        #serializer.save(creator=creator)
        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)

class deleteItem(generics.DestroyAPIView):
    queryset = Item.objects.all()
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id' #id of the item

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()  # Get the item instance to be deleted
        self.perform_destroy(instance)
        return Response({"message": "Item deleted successfully"})

class highestBid(APIView):
    permission_classes = [AllowAny]
    lookup_field = 'id'

    #should also return id of highest bidder
    def get(self, request, *args, **kwargs):
        item = self.kwargs['id'] #item is assigned to the id num

        #highest_bid = Bid.objects.filter(item=item).order_by('-bid_price').first()
        highest_bid = Bid.objects.filter(item=item, won=True).first()
        highest_bid_amount = highest_bid.bid_price if highest_bid else None
        highest_bidder = highest_bid.bidder.id if highest_bid else None

        data = {
            'item_id': item,
            'bidder': highest_bidder,
            'highest_bid': highest_bid_amount,
        }

        return Response(data, status=status.HTTP_200_OK)
    
class categoryItems(generics.RetrieveAPIView):
    queryset = Item.objects.active_items()
    serializer_class = serializers.ItemSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = self.request.user
            cat = self.kwargs['cat'] #the url sends the category as string
            items = Item.objects.active_items().filter(
                creator=user,
                category=cat
            ).order_by('-end_time')
            serializer = serializers.ItemSerializer(items, many=True)
            return Response(serializer.data)
        except Exception as e:
            error_message = str(e)
            return Response({'error': error_message}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)