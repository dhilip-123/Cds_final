from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Community,ElectionOfficer,CommunityAdmin

class CommunitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Community
        fields = ['id', 'name', 'address', 'purpose', 'mission', 'vision']

class CreateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password']
        )
        return user
    
class CommunityAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommunityAdmin
        fields = ['id','user', 'community']  
    
class ElectionOfficerSerializer(serializers.ModelSerializer):
    community = serializers.PrimaryKeyRelatedField(queryset=Community.objects.all())
    
    class Meta:
        model = ElectionOfficer
        fields = ['id', 'community', 'user']
