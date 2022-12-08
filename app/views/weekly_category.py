from rest_framework import status, permissions, viewsets
from rest_framework.decorators import APIView
from rest_framework.response import Response
from ..models import WeeklyCategory, WeeklyExpense, MonthlyIncome
from ..serializers import  WeeklyCategorySerializer
from ..utils import get_auth_token
from django.http import Http404
from ..task import update_expense_income_amount

class WeeklyCategoryList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request, format=None):
        weekly_categories = WeeklyCategory.objects.filter(user=request.user)
        serializer = WeeklyCategorySerializer(weekly_categories, many=True)
        return Response(serializer.data)
    
    def post(self, request, format=None):
        token = get_auth_token(request)
        serializer = WeeklyCategorySerializer(data=request.data, context=token)
        if serializer.is_valid():
            serializer.save()
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WeeklyCategoryDetail(APIView):
    permissions_classes = [permissions.IsAuthenticated]
    def get_category(self, pk):
        try:
            return WeeklyCategory.objects.get(pk=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    
    def get(self, request, pk, format=None):
        category = self.get_category(pk)
        serializer = WeeklyCategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_302_FOUND)
    
    def put(self, request, pk, format=None):
        category = self.get_category(pk)
        # update_expense_income_amount.delay(category_id=category.id, category_week=category.week, category_year=category.year, category_month=category.month, amount=request.data['amount'])
        update_expense_income_amount(category_id=category.id, category_week=category.week, category_year=category.year, category_month=category.month, amount=request.data['amount'])
        serializer = WeeklyCategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



