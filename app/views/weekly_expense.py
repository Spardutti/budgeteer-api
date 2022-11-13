from rest_framework import status, permissions
from rest_framework.decorators import APIView
from rest_framework.response import Response
from ..models import  WeeklyExpense
from ..serializers import WeeklyExpenseSerializer

class WeeklyExpenseList(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def get(self, request, format=None):
        weekly_expenses = WeeklyExpense.objects.all()
        serializer = WeeklyExpenseSerializer(weekly_expenses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request, format=None):
        serializer = WeeklyExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)