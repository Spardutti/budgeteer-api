from .models import CustomUser, MonthlyIncome, WeeklyCategory, WeeklyExpense
from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from datetime import datetime
from .utils import week_of_month

class UserSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(many=True, queryset=WeeklyCategory.objects.all(), required=False)
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'categories', 'password', 'amount']
        extra_kwargs = {'password': {'write_only': True}}


    def create(self, validated_data):
        user = CustomUser.objects.create(
            username = validated_data['username'],
            password = make_password(validated_data['password'])
        )
        user.save()
        return user



class WeeklyCategorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True, required=False, source='user.username')
    week = serializers.ReadOnlyField()
    year = serializers.ReadOnlyField()
    month = serializers.ReadOnlyField()
    class Meta:
        model = WeeklyCategory
        fields = ['id', 'name', 'user', 'week', 'month', 'week', 'amount', 'year']

    def create(self, validated_data):
        user = self.context
        name = validated_data['name']
        now = datetime.now()
        year = now.year
        month = now.month
        week = week_of_month()
        data = {'user': user, 'year': year, 'month': month, 'week': week, 'name': name}
        category = WeeklyCategory.objects.create(**data)
        
        return category
 
class WeeklyExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyExpense
        fields = ['user', 'weekly_category', 'amount', 'id']
    
    def create(self, validated_data):
        weekly_expense = WeeklyExpense.objects.create(**validated_data)
        return weekly_expense

class MonthlyIncomeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = MonthlyIncome
        fields = '__all__'
    
    def create(self, validated_data):
        user = self.context['user']
        get_user = CustomUser.objects.get(pk=user)
      
        category = MonthlyIncome.objects.create(user=get_user, **validated_data)
        
        return category
