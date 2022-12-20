from ..models import CustomUser
from rest_framework import serializers
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username',  'password', 'amount']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = CustomUser.objects.create(
            username = validated_data['username'],
            password = make_password(validated_data['password'])
        )
        user.save()
        return user