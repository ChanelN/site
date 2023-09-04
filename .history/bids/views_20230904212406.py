from django.shortcuts import render
from .models import Item, User, Bid
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from . import serializers
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.utils import timezone

class BidViewset(ModelViewSet):
    queryset = Bid.objects.all()
    serializer_class = serializers.BidSerializer
    authentication_classes = []
    permission_classes = []

#view to MAKE a bid - post
#validate both creator and bidder - 
class MakeBid(generics.CreateAPIView):
    queryset = Bid.objects.all()
    serializer_class = serializers.BidSerializer
    permission_classes = [IsAuthenticated]

    def post(self,request, format=None):
        #http_x is in the headers

        creator = self.request.data.get('creator')
        try:
            creator = User.objects.get(id=creator)   #try find the user
        except User.DoesNotExist:
            return Response({'message': 'Invalid creator id'}, status=status.HTTP_400_BAD_REQUEST)
        
        bidder = self.request.data.get('bidder')
        try:
            bidder = User.objects.get(id=bidder)   #try find the user
        except User.DoesNotExist:
            return Response({'message': 'Invalid bidder id'}, status=status.HTTP_400_BAD_REQUEST)

        item_id = self.request.data.get('item')
        try:
            item = Item.objects.active_items().get(id=item_id)  # Retrieve the Item instance
        except Item.DoesNotExist:
            return Response({'message': 'Invalid item id'}, status=status.HTTP_400_BAD_REQUEST)
        
        now = timezone.now()
        previous_highest_bid = Bid.objects.filter(item=item, won=True).first()
        if previous_highest_bid:
            previous_highest_bid.won = False
            previous_highest_bid.save()

        serializer = serializers.BidSerializer(data=request.data)
        if(serializer.is_valid()):
            bid = serializer.save(creator=creator, bidder=bidder, item=item)
            if item.end_time > now:
                bid.won = True
                bid.save()
            return Response({'message': 'Bid placed', 'bid_id': bid.id}, status= status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
class UpdateBid(generics.UpdateAPIView):
    #so identify the bid through the bidder id? 
    queryset = Bid.objects.all()
    serializer_class = serializers.BidSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'bidder'

    def put(self,request, *args, **kwargs):
        bid = self.get_object() #it should retrieve item based on id field based in url

        serializer = self.get_serializer(bid, data = self.request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        self.perform_update(serializer)
        return Response(serializer.data, status=status.HTTP_200_OK)
