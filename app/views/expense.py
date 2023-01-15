from rest_framework import viewsets, permissions, status
from ..models import Expense, Category
from ..serializers import ExpenseSerializer
from rest_framework.decorators import  action
from rest_framework.response import Response
from ..utils import get_auth_token

class ExpenseSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer

    # @action(detail=True, methods=['POST'])
    def create(self, request):
        user = get_auth_token(request)
        category = Category.objects.filter(user=user, id=request.data['category']).first()
        serializer = self.get_serializer(data=request.data, context=category)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def list(self, request):
        category = Category.objects.filter(user=request.user.id, id=request.query_params['category_id']).first()
        expenses = Expense.objects.filter( category=category).order_by('date')
        serializer = self.get_serializer(expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

## TODO get all expense of a specific month
    # @action(detail=False, methods=['GET'])
    # def category_expense(self, request):
    #     category_id = request.query_params.get('id')
    #     expenses = Expense.objects.filter(weekly_category=category_id)
    #     serializer = self.get_serializer(expenses, many=True)
    #     return Response(serializer.data, status=status.HTTP_200_OK)
    #     #TODO we got the detail in postman!!