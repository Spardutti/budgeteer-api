from rest_framework import status, permissions, viewsets
from rest_framework.response import Response
# from ..task import create_monthly_income_login, create_weekly_category_login
from ..models import CustomUser
from ..serializers import UserSerializer

class UserSet(viewsets.ModelViewSet):
    def get_permissions(self):
        if self.action == "create":
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]  

    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

    def partial_update(self, request, *args, **kwargs):
        try:
            user = request.user
            amount = int(request.data['amount'])
            user.amount = amount
            serializer = self.get_serializer(user, partial=True)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response("error", status=status.HTTP_400_BAD_REQUEST)
       
    def retrieve(self, request, pk):
        serializer = self.get_serializer(request.user)
        user = request.user
        # if not user.is_superuser:
            # create_monthly_income_login(user.id, user.amount)
            # create_weekly_category_login(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)