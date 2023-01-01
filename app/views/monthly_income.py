from rest_framework import status, permissions, viewsets
from rest_framework.decorators import  action
from rest_framework.response import Response
from ..models import MonthlyIncome
from ..serializers import MonthlyIncomeSerializer

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

    @action(detail=True, methods=['get'])
    def monthly(self, request,  *args, **kwargs):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        income = MonthlyIncome.objects.filter(month=month, year=year, user=request.user.id).first()
        serializer = self.get_serializer(income)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["PATCH"], detail=True)
    def account_balance(self, request, pk=None):
        today = datetime.now()
        month = today.month
        year = today.year
        user_id = request.user.id
        account_balance = int(request.data['account_balance'])
        monthly_income = MonthlyIncome.objects.filter(year=year, month=month, user=user_id).first()
        monthly_income.account_balance = account_balance
        serializer = self.get_serializer(monthly_income)
        monthly_income.save()
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
        if request.data['account_balance']:
            balance = int(request.data['account_balance'])
            if monthly_income.account_balance == 0:
                monthly_income.account_balance = balance
            else:
                monthly_income.account_balance -= balance
        serializer = self.get_serializer(monthly_income)
        monthly_income.save()
        return Response(serializer.data, status=status.HTTP_200_OK)