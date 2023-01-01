from ..models import  WeeklyExpense
from rest_framework import serializers


class WeeklyExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyExpense
        fields = ['user', 'weekly_category', 'amount', 'id']
    