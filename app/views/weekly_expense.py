from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..models import  WeeklyExpense
from ..serializers import WeeklyExpenseSerializer

class WeeklyExpenseSet(viewsets.ModelViewSet):
    permission_classes = [ permissions.IsAuthenticatedOrReadOnly]
    queryset = WeeklyExpense.objects.all()
    serializer_class = WeeklyExpenseSerializer
    
    def list(self, request, *args, **kwargs):
        weekly_expense = WeeklyExpense.objects.filter(user=request.user.id)
        serializer = self.get_serializer(weekly_expense, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)