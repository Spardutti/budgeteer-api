from rest_framework import status, permissions, viewsets
from rest_framework.decorators import  action
from rest_framework.response import Response
from ..models import Category
from ..serializers import CategorySerializer
from ..utils import get_auth_token

class CategorySet(viewsets.ModelViewSet):
    permission_classes = [ permissions.IsAuthenticatedOrReadOnly]

    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def list(self, request, *args, **kwargs):
        categories = Category.objects.filter(user=request.user.id)
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def monthly(self, request,  *args, **kwargs):
        month = int(request.query_params.get('month'))
        year = int(request.query_params.get('year'))
        categories = Category.objects.filter(date__year=year, date__month=month, user=request.user.id).order_by('position')
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(["GET"], detail=False)
    def unique_months(self, request, pk=None):
        user_id = request.user.id
        months = Category.objects.filter(user=user_id).values('date__month', 'date__year').distinct()
        return Response(months, status=status.HTTP_200_OK)

    def create(self, request):
        token = get_auth_token(request)
        if Category.objects.filter(user=token, name=request.data['name']):
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
