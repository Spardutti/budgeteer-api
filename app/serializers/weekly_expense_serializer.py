from ..models import  WeeklyExpense
from rest_framework import serializers


class WeeklyExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyExpense
        fields = ['user', 'weekly_category', 'amount', 'id']
    
    def create(self, validated_data):
        weekly_expense = WeeklyExpense.objects.create(**validated_data)
        return weekly_expense