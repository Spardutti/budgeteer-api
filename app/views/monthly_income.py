from rest_framework import status, permissions, viewsets
from rest_framework.decorators import APIView, action
from rest_framework.response import Response
from ..models import MonthlyIncome
from ..serializers import MonthlyIncomeSerializer
from ..utils import get_auth_token
from django.http import Http404
from datetime import datetime


class MonthlyIncomeSet(viewsets.ModelViewSet):
    permission_classes = [ permissions.IsAuthenticatedOrReadOnly]
    queryset = MonthlyIncome.objects.all()
    serializer_class = MonthlyIncomeSerializer

    def list(self, request, *args, **kwargs):
        monthly_income = MonthlyIncome.objects.filter(user=request.user.id)
        seriazlier = self.get_serializer(monthly_income, many=True)
        return Response(seriazlier.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk):
        today = datetime.now()
        month = today.month
        year = today.year
        user_id = request.user.id
        monthly_income = MonthlyIncome.objects.filter(year=year, month=month, user=user_id).first()
        serializer = self.get_serializer(monthly_income)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        today = datetime.now()
        month = today.month
        year = today.year
        user_id = request.user.id
        amount = int(request.data['amount'])
        monthly_income = MonthlyIncome.objects.filter(year=year, month=month, user=user_id).first()
        if monthly_income.amount == 0:
            monthly_income.amount = amount
        else:
            monthly_income.amount -= amount
        serializer = self.get_serializer(monthly_income)
        monthly_income.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

# class MonthlyIncomeList(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
#     def get(self, request, format=None):
#         monthly_income = MonthlyIncome.objects.all()
#         serializer = MonthlyIncomeSerializer(monthly_income, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def post(self, request, format=None):
#         token = get_auth_token(request)
#         serializer = MonthlyIncomeSerializer(data=request.data, context=token)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class MonthlyIncomeDetail(APIView):
#     def get_income(self, pk):
#         try:
#             return MonthlyIncome.objects.get(pk=pk)
#         except MonthlyIncome.DoesNotExist:
#             return Http404
    
#     def put(self, request, pk, format=None):
#         income = self.get_income(pk)
#         serializer = MonthlyIncomeSerializer(income, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        