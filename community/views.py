from rest_framework import viewsets, status
from rest_framework.response import Response
from django.core.mail import send_mail
from rest_framework.decorators import api_view,permission_classes
# from rest_framework.permissions import AllowAny
from django.conf import settings
from .models import Community, ElectionOfficer, CommunityAdmin
from django.contrib.auth.models import User
from .serializers import CommunitySerializer, CreateUserSerializer, ElectionOfficerSerializer, CommunityAdminSerializer
from drf_yasg.utils import swagger_auto_schema

class CommunityViewSet(viewsets.ModelViewSet):
    queryset = Community.objects.all()
    serializer_class = CommunitySerializer

    @swagger_auto_schema(request_body=CommunitySerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        
        # Send email to the user
        send_mail(
            'User Registration for CDS',
            'You have been successfully registered.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

class CommunityAdminViewSet(viewsets.ModelViewSet):
    queryset = CommunityAdmin.objects.all()
    serializer_class = CommunityAdminSerializer

    @swagger_auto_schema(request_body=CommunityAdminSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user_id = request.data.get('user')
        community_id = request.data.get('community')
        password = request.data.get('password')
        
        try:
            user = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response({'detail': f'User with ID {user_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            return Response({'detail': f'Community with ID {community_id} does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        community_admin = serializer.save(user=user, community=community)
        
        # Send email to the Community Admin
        send_mail(
            'Community Admin Login Credentials',
            f'Username: {user.email}\nPassword: {password if password else "password used at time of Registration"}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ElectionOfficerViewSet(viewsets.ModelViewSet):
    queryset = ElectionOfficer.objects.all()
    serializer_class = ElectionOfficerSerializer

    @swagger_auto_schema(request_body=ElectionOfficerSerializer)
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        community_id = request.data.get('community')
        
        try:
            community = Community.objects.get(pk=community_id)
        except Community.DoesNotExist:
            return Response({'detail': 'Community with this ID does not exist.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user = serializer.validated_data.get('user')
        election_officer = serializer.save(community=community)
        
        # Send email to the Election Officer
        send_mail(
            'Election Officer Login Credentials',
            f'Username: {user.email}\nPassword: {request.data.get("password")}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        
        response_serializer = self.get_serializer(instance=election_officer)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
