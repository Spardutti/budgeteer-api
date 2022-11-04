from rest_framework import status, permissions
from rest_framework.decorators import APIView
from rest_framework.response import Response

from .task import create_weekly_expense
from .models import CustomUser, MonthlyIncome, WeeklyCategory, WeeklyExpense
from .serializers import MonthlyIncomeSerializer, UserSerializer, WeeklyCategorySerializer, WeeklyExpenseSerializer
from django.http import Http404
from rest_framework_simplejwt.authentication import JWTAuthentication
from .utils import week_of_month

# Create your views here.
jwt_auth = JWTAuthentication()

def get_auth_token( request):
        token = jwt_auth.authenticate(request)[0]
        return token

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
        return Response(serializer.data)
    
    def put(self, request, pk, format=None):
        user = self.get_user(pk)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        user = self.get_user(pk)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class WeeklyCategoryList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        weekly_categories = WeeklyCategory.objects.all()
        serializer = WeeklyCategorySerializer(weekly_categories, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        token = get_auth_token(request)
        serializer = WeeklyCategorySerializer(data=request.data, context=token)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class WeeklyExpenseList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        weekly_expenses = WeeklyExpense.objects.all()
        serializer = WeeklyExpenseSerializer(weekly_expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = WeeklyExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MonthlyIncomeList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get(self, request, format=None):
        monthly_income = MonthlyIncome.objects.all()
        serializer = MonthlyIncomeSerializer(monthly_income, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        token = get_auth_token(request)
        serializer = MonthlyIncomeSerializer(data=request.data, context=token)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)