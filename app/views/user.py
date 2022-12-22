from rest_framework import status, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from ..task import create_monthly_income_login, create_weekly_category_login
from datetime import datetime
from ..utils import week_of_month
from ..models import CustomUser, MonthlyIncome
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
            user.amount = request.data['amount']
            serializer = self.get_serializer(user, partial=True)
            user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response('error', status=status.HTTP_400_BAD_REQUEST)
       
    def retrieve(self, request, pk):
        serializer = self.get_serializer(request.user)
        user = request.user
        if not user.is_superuser:
            create_monthly_income_login(user.id, user.amount)
            create_weekly_category_login(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def destroy(self, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        super().destroy(*args, **kwargs)
        return Response(serializer.data, status=status.HTTP_200_OK)



    # def post(self, request):

# def get_permissions(self):
#     """Returns the permission based on the type of action"""

#     if self.action == "create":
#         return [permissions.AllowAny()]

#     return [permissions.IsAuthenticated()]  
    # def get(self, request, format=None):
    #     users = CustomUser.objects.all()
    #     serializer = UserSerializer(users, many=True)
    #     return Response(serializer.data)
    
    # def post(self, request, format=None):
    #     serializer = UserSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class UserDetail(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get_user(self, pk):
#         try:
#             return CustomUser.objects.get(pk=pk)
#         except CustomUser.DoesNotExist:
#             raise Http404
    
#     def get(self, request, format=None):
#         user = self.get_user(request.user.id)
#         serializer = UserSerializer(user)
#         # create_monthly_income_login.delay(user.id, user.amount)
#         # create_weekly_category_login.delay(user.id)
#         create_monthly_income_login(user.id, user.amount)
#         create_weekly_category_login(user)
#         return Response(serializer.data)
    
#     def put(self, request, pk, format=None):
#         user = self.get_user(pk)
#         serializer = UserSerializer(user, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     def delete(self, request, pk, format=None):
#         user = self.get_user(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)