# from .models import CustomUser, MonthlyIncome, WeeklyCategory, WeeklyExpense
# from rest_framework import serializers
# from django.contrib.auth.hashers import make_password
# from datetime import datetime
# from .utils import week_of_month

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CustomUser
#         fields = ['id', 'username',  'password', 'amount']
#         extra_kwargs = {'password': {'write_only': True}}


#     def create(self, validated_data):
#         user = CustomUser.objects.create(
#             username = validated_data['username'],
#             password = make_password(validated_data['password'])
#         )
#         user.save()
#         return user




# class WeeklyExpenseSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = WeeklyExpense
#         fields = ['user', 'weekly_category', 'amount', 'id']
    
#     def create(self, validated_data):
#         weekly_expense = WeeklyExpense.objects.create(**validated_data)
#         return weekly_expense

# class MonthlyIncomeSerializer(serializers.ModelSerializer):
#     user = serializers.ReadOnlyField(source='user.username')
    
#     class Meta:
#         model = MonthlyIncome
#         fields = '__all__'
    
#     def create(self, validated_data):
#         user = self.context['user']
#         get_user = CustomUser.objects.get(pk=user)
      
#         category = MonthlyIncome.objects.create(user=get_user, **validated_data)
        
#         return category
