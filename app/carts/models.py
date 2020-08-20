from django.db import models
from django.conf import settings

from products.models import Product


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # product_variations = models.ManyToManyField(ProductVariation)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        # TODO: Remove the id
        return f"({self.id}) {self.quantity} {self.product.title}"
        # return f"({self.id}) {self.quantity} {self.product.title}, sized {self.product_variations.first()}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_final_price(self):
        return self.get_total_product_price()
