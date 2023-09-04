from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Item, User, Bid

class BidSerializer(serializers.ModelSerializer):
    #so primaryKeyRelatedField means it only links using the primary key of customUser(the userId)
    #the readable field is to return in the serialized output
    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    creator_readable = serializers.StringRelatedField(read_only=True) #human readable rep

    bidder = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    bidder_readable = serializers.StringRelatedField(read_only=True) #human readable rep

    item = serializers.PrimaryKeyRelatedField(queryset=Item.objects.all(), write_only=True)
    item_readable = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Bid
        fields = ['creator', 'creator_readable', 'bidder', 'bidder_readable', 'item', 'item_readable', 'bid_price', 'bid_time', 'won']

    def validate(self, data):
        bidder = data['bidder']
        creator = data['creator']

        if bidder == creator:
            raise serializers.ValidationError("The creator of the item cannot bid on it.")

        return data