from rest_framework.generics import (
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
)
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import (
    SAFE_METHODS,
    IsAdminUser,
)

from products.models import Product
from products.api.serializers import ProductSerializer

from inventory.models import InventoryItem


class PermissionMixin:

    def get_permissions(self):
        if not self.request.method in SAFE_METHODS:
            self.permission_classes = [IsAdminUser]
        return super().get_permissions()


class ProductListView(PermissionMixin, ListCreateAPIView):
    model = Product
    queryset = model.objects.all()
    serializer_class = ProductSerializer

    def post(self, request, *args, **kwargs):
        serializer = ProductSerializer(data=request.data,
                                       context={'request': request})
        if serializer.is_valid():
            vendor = request.user
            serializer.validated_data['vendor'] = vendor
            product = serializer.save()
            InventoryItem.objects.create(
                product=product,
                quantity=int(request.data.get('quantity', 1)),
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get('all', False) is False:
            queryset = queryset.filter(available=True, inventory__quantity__gt=0)
        return super().get_queryset()


class ProductSingleView(PermissionMixin, RetrieveUpdateDestroyAPIView):
    model = Product
    queryset = model.objects.all()
    serializer_class = ProductSerializer

    def perform_destroy(self, instance):
        inventory_item = instance.inventory
        inventory_item.quantity = 0
        inventory_item.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(available=True, inventory__quantity__gt=0)
        return queryset

    def delete(self, request, *args, **kwargs):
        super().delete(request, *args, **kwargs)
        return Response({'message': 'Product inventory set to 0'},
                        status=status.HTTP_200_OK)
