from rest_framework import status, permissions, viewsets
from rest_framework.decorators import  action
from rest_framework.response import Response
from ..models import WeeklyCategory
from ..serializers import WeeklyCategorySerializer
from ..utils import get_auth_token
from ..task import update_expense_income_amount
import json

class WeeklyCategorySet(viewsets.ModelViewSet):
    permission_classes = [ permissions.IsAuthenticatedOrReadOnly]

    serializer_class = WeeklyCategorySerializer
    queryset = WeeklyCategory.objects.all()

    def list(self, request, *args, **kwargs):
        categories = WeeklyCategory.objects.filter(user=request.user.id)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def monthly(self, request,  *args, **kwargs):
        month = request.query_params.get('month')
        year = request.query_params.get('year')
        categories = WeeklyCategory.objects.filter(month=month, year=year, user=request.user.id).order_by('id')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["GET"], detail=False)
    def unique_months(self, request, pk=None):
        user_id = request.user.id
        months = WeeklyCategory.objects.filter(user=user_id).values('month', 'year').distinct()
        return Response(months, status=status.HTTP_200_OK)

    def create(self, request):
        token = get_auth_token(request)
        if WeeklyCategory.objects.filter(user=token, name=request.data['name']):
            return Response({'Error': 'This name already exist'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data, context=token)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, *args, **kwargs):
        try:
            category = self.get_object()
            data = json.loads(request.body)
            category.amount += int(data['amount'])
            # update_expense_income_amount.delay(category_id=category.id, category_week=category.week, category_year=category.year, category_month=category.month, amount=request.data['amount'])
            update_expense_income_amount(category_id=category.id,  category_year=category.year, category_month=category.month, amount=int(data['amount']), user_id=request.user.id)
            serializer = self.get_serializer(category, partial=True)
            category.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(str(e), status=status.HTTP_400_BAD_REQUEST)