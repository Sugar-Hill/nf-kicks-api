from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save
from django.dispatch import receiver

from products.models import Size


# Create your models here.
class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} {self.size.product.title}, sized {self.size.size}"

    def get_total_product_price(self):
        return self.quantity * self.size.product.price

    def get_final_price(self):
        return self.get_total_product_price()


@receiver(pre_save, sender=CartItem)
def decrease_stock_receiver(sender, instance, *args, **kwargs):
    if instance.ordered is True:
        size = instance.size
        size.stock -= instance.quantity
        size.save()
