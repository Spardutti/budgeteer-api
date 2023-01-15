from ..models import Expense
from rest_framework import serializers
import datetime

class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(many=False, read_only=True, source='category.name')
    
    class Meta:
        model = Expense
        fields = ['id', 'amount', 'description', 'category', 'date']
    
    def create(self, validated_data):
        category = self.context
        amount = validated_data.get('amount', 0)
        description = validated_data.get('description', '')
        date = datetime.date.today()
        data = {'category': category, 'date': date, 'amount': amount, 'description': description }
        category = Expense.objects.create(**data)
        
        return category