from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from inventory.models import InventoryItem
from inventory.api.serializers import InventoryItemSerializer

from tests.helpers import (
    AccountsTestHelpers,
    CategoriesTestHelpers,
    ProductsTestHelpers,
    InventoryTestHelpers,
)


class SetUpTestCase(TestCase):

    def authenticate(self):
        self.client = APIClient()
        self.client.force_authenticate(user=self.vendor)

    def create_related_objects(self):
        self.vendor = AccountsTestHelpers().create_vendor()
        category = CategoriesTestHelpers().create_category()
        self.product = ProductsTestHelpers().create_product(
            vendor=self.vendor, category=category
        )
        self.inevntory_item = InventoryTestHelpers().create_inventory_item(
            product=self.product, quantity=10,
        )

    def setUp(self):
        self.create_related_objects()
        self.authenticate()


class InventoryItemListEndpointTestCase(SetUpTestCase):

    def test_get(self):
        response = self.client.get(reverse('inventory-items'))
        serializer = InventoryItemSerializer(InventoryItem.objects.all(),
                                             many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(InventoryItem.objects.count(), 1)
