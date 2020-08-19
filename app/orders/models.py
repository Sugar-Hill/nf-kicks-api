from django.db import models
from django.db.models.signals import post_save
from django.conf import settings

from products.models import Product, ProductVariation
from payments.models import Payment


# Create your models here.
ORDER_STATUS = (
    ('I', 'In Cart'),
    ('O', 'Ordered'),
    ('F', 'Fulfilled'),
    ('C', 'Completed')
)

REFUND_STATUS = (
    ('N', 'None'),
    ('R', 'Requested'),
    ('G', 'Granted')
)


class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_variations = models.ManyToManyField(ProductVariation)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        # TODO: Remove the id
        return f"({self.id}) {self.quantity} {self.product.title}, sized {self.product_variations.first()}"

    def get_total_product_price(self):
        return self.quantity * self.product.price

    def get_final_price(self):
        return self.get_total_product_price()


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    order_status = models.CharField(
        choices=ORDER_STATUS, default='I', max_length=2)
    payment = models.ForeignKey(
        Payment, on_delete=models.SET_NULL, blank=True, null=True)

    refund_status = models.CharField(choices=REFUND_STATUS, default=1, max_length=2)

    def __str__(self):
        # TODO: Might be the reason payment is not working
        return self.user.email

    def get_total(self):
        total = 0
        for cart_item in self.cart_items.all():
            total += cart_item.get_final_price()
        return total


# def decrease_stock_receiver(sender, instance, created, *args, **kwargs):
#     if created:
#         for productVariation in instance.order_items.product_variations:
#             productVariation.stock -= productVariation.stock


# post_save.connect(decrease_stock_receiver, sender=Order)
