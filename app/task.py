from celery import shared_task
from rest_framework.response import Response
from rest_framework import status
from .serializers import WeeklyExpenseSerializer, MonthlyIncomeSerializer, WeeklyCategorySerializer
from datetime import datetime
from .utils import week_of_month
from datetime import datetime
from .models import MonthlyIncome, WeeklyCategory, WeeklyExpense

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

@shared_task
def update_expense_income_amount(category_id, category_week, category_year, category_month, amount):
    weekly_expense = WeeklyExpense.objects.get(weekly_category=category_id)
    monthly_income = MonthlyIncome.objects.get(user=weekly_expense.user.id, week=category_week, year=category_year, month=category_month)
    weekly_expense.amount += amount
    monthly_income.amount -=amount

    weekly_expense.save()
    monthly_income.save()
    return status.HTTP_200_OK

@shared_task
def create_monthly_income_login(user_id, user_amount):
    today = datetime.now()
    month = today.month
    year = today.year
    week = week_of_month()
    
    montly_income = MonthlyIncome.objects.filter(user=user_id, year=year, month=month).first()
    if montly_income is None:
        data = { 'year':year, 'month': month, 'week': week, 'amount': user_amount if user_amount else 0 }
        context = {'user': user_id,}
        serializer = MonthlyIncomeSerializer(data=data, context=context)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@shared_task
def create_weekly_category_login(user_id):
    today = datetime.now()
    month = today.month
    year = today.year
    week = week_of_month()
    weekly_categories = WeeklyCategory.objects.filter(user=user_id)
    if len(weekly_categories) > 0:
        for category in weekly_categories:
            if category.month != month and category.week != week and category.year != year:
                data = { 'year': year, 'month': month, 'week': week, 'name': category.name }
                context = {'user': user_id}
                serializer = WeeklyCategorySerializer(data=data, context=context)
                if serializer.is_valid():
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_200_OK)



