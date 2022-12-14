from ..models import CustomUser, MonthlyIncome
from rest_framework import serializers

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