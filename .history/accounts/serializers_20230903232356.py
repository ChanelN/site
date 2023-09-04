from rest_framework import serializers
from django.contrib.auth import authenticate
from .models import User
from rest_framework.validators import UniqueValidator

'''serializers are used for dealing with model instances and querysets
serialiser can transform the data from MODEL to JSON

'''
class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(validators=[UniqueValidator(queryset=CustomUser.objects.all())])
    image = serializers.ImageField(required=False)
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False, min_length=8)
    
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            #so that when updating user profile, they dont have to send username and pass with every request
            'password': {'required': False},
            'email': {'required': False},
        }

    def create(self, validated_data):
        '''
        password = validated_data.pop('password', None)
        is_active = validated_data.pop('is_active', True)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
        '''
        user =  User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            dob=validated_data['dob'],
        )
        user.save()
        return user

    def update(self, instance, validated_data):
        '''
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        '''
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()
        return instance
    '''
        current_password = validated_data.get("current_password")
        new_password = validated_data.get("new_password")
        if current_password and new_password:
            # Check if the current password is correct
            if not instance.check_password(current_password):
                raise serializers.ValidationError("Current password is incorrect.")
            instance.set_password(new_password)

        instance.save()
        return instance
    '''
    '''
    def update(self, instance, validated_data):
         # We try to get profile data
        profile_data = validated_data.pop('profile', None)
        # If we have one
        if profile_data is not None:
            # We set address, assuming that you always set address
            # if you provide profile
            instance.profile.address = profile_data['address']
            # And save profile
            instance.profile.save()
        # Rest will be handled by DRF
        return super().update(instance, validated_data)
        
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance
        '''

#use this serializer to session login
#sending a httpPOST to the loginview acc works
class LoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * username
      * password.
    It will try to authenticate the user with when validated.
    """
    email = serializers.CharField(
        label="Email",
        write_only=True
    )
    password = serializers.CharField(
        label="Password",
        # This will be used when the DRF browsable API is enabled
        style={'input_type': 'password'},
        trim_whitespace=False,
        write_only=True
    )

    def validate(self, attrs):
        # Take username and password from request
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            # Try to authenticate the user using Django auth framework.
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)
            if not user:
                # If we don't have a regular user, raise a ValidationError
                msg = 'Access denied: wrong username or password.'
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = 'Both "username" and "password" are required.'
            raise serializers.ValidationError(msg, code='authorization')
        # We have a valid user, put it in the serializer's validated_data.
        # It will be used in the view.
        attrs['user'] = user
        return attrs