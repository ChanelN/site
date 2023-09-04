from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import Item, User

class ItemSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True)
    starting_price = serializers.DecimalField(required=True, max_digits=10, decimal_places=2)
    end_time = serializers.DateTimeField(required=True)

    creator = serializers.PrimaryKeyRelatedField(queryset=User.objects.all()) #write only
    creator_readable = serializers.StringRelatedField(read_only=True) #human readable rep

    class Meta:
        model = Item
        fields = '__all__'

    def create(self, validated_data):
        creator = validated_data.get('creator')  # Remove email from validated_data
        validated_data['creator'] = creator
        return super().create(validated_data)
        '''
        user = CustomUser.objects.get(id=creator)
        validated_data['creator'] = user  # Replace email with user instance
        return super().create(validated_data)
        '''
    def update(self, instance, validated_data):
        #doesn't need user if we're passsing specific itemID
        creator = validated_data.pop('creator')
        if creator:
            #user = CustomUser.objects.get(id=creator)
            instance.creator = creator #or user
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance