from ..models import  Category
from rest_framework import serializers
import datetime
from ..utils import week_of_month


class CategorySerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(many=False, read_only=True, required=False, source='user.username')
    class Meta: 
        model = Category
        fields = ['id', 'name', 'user', 'date', 'budget', 'position', 'is_deleted']

    def create(self, validated_data):
        user = self.context
        name = validated_data['name']
        date = datetime.date.today()
        data = {'user': user, 'date': date, 'name': name }
        category = Category.objects.create(**data)
        
        return category
 