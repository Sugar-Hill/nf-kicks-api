from django.db import models
from django.conf import settings

from carts.models import CartItem
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


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date = models.DateTimeField(blank=True, null=True)
    order_status = models.CharField(
        choices=ORDER_STATUS, default='I', max_length=2)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, blank=True, null=True)

    refund_status = models.CharField(
        choices=REFUND_STATUS, default='N', max_length=2)

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
