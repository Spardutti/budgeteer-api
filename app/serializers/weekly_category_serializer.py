from ..models import  WeeklyCategory
from rest_framework import serializers
from datetime import datetime
from ..utils import week_of_month


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
 