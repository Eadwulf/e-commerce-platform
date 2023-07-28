from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=128)
    brand = models.CharField(max_length=128)
    image_url = models.CharField(default='',
                             max_length=512,
                             null=True,
                             blank=True)
    description = models.CharField(max_length=512)
    specifications = models.JSONField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    vendor = models.ForeignKey('accounts.User',
                               on_delete=models.PROTECT,
                               related_name='products')
    category = models.ForeignKey('categories.Category',
                                 on_delete=models.PROTECT,
                                 related_name='products',
                                 blank=True,
                                 null=True)
    available = models.BooleanField(default=True)

    class Meta:
        unique_together = ['vendor', 'name']

    def __str__(self) -> str:
        return self.name


class DeletedProduct(models.Model):
    product = models.ForeignKey('products.product',
                                on_delete=models.PROTECT,
                                related_name='deleted_products')
    deleted_by = models.ForeignKey('accounts.user',
                                    on_delete=models.PROTECT,
                                    related_name='deleted_products')
    deleted_on = models.DateTimeField(auto_now_add=True)
