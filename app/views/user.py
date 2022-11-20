from rest_framework import status, permissions
from rest_framework.decorators import APIView
from rest_framework.response import Response

from ..models import CustomUser
from ..serializers import UserSerializer
from django.http import Http404
from ..utils import get_auth_token
from ..task import create_monthly_income_login, create_weekly_category_login

class UserList(APIView):
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        users = CustomUser.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetail(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_user(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404
    
    def get(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = UserSerializer(user)
        # create_monthly_income_login.delay(user.id, user.amount)
        # create_weekly_category_login.delay(user.id)
        create_monthly_income_login(user.id, user.amount)
        create_weekly_category_login(user.id)
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        user = self.get_user(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)