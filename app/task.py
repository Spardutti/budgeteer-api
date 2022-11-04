from celery import shared_task
from rest_framework.response import Response
from rest_framework import status
from .serializers import WeeklyExpenseSerializer, MonthlyIncomeSerializer
from datetime import datetime
from .utils import week_of_month

@shared_task
def create_weekly_expense(user_id, category_id):
    data = {'user': user_id, 'weekly_category': category_id, 'amount': 0}
    serializer = WeeklyExpenseSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@shared_task
def create_monthly_income(user_id, user_amount):
    today = datetime.now()
    year = today.year
    month = today.month
    week = week_of_month()
    data = {'amount': user_amount, 'year': year, 'month': month, 'week': week}
    context = {'user': user_id}
    serializer = MonthlyIncomeSerializer(data=data, context=context)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


