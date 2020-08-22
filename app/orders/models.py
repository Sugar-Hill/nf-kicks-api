from django.db import models
from django.conf import settings

from carts.models import CartItem
from payments.models import Payment

# Create your models here.
ORDER_STATUS = (
    ('In Cart', 'In Cart'),
    ('Ordered', 'Ordered'),
    ('Fulfilled', 'Fulfilled'),
    ('Completed', 'Completed')
)

REFUND_STATUS = (
    ('None', 'None'),
    ('Requested', 'Requested'),
    ('Granted', 'Granted')
)


class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(CartItem)
    start_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(
        choices=ORDER_STATUS, default='In Cart', max_length=9)
    payment = models.ForeignKey(
        Payment, on_delete=models.CASCADE, blank=True, null=True)
    refund_status = models.CharField(
        choices=REFUND_STATUS, default='None', max_length=9)

    def __str__(self):
        # TODO: Might be the reason payment is not working
        return self.user.email

    def get_total(self):
        total = 0
        for cart_item in self.cart_items.all():
            total += cart_item.get_final_price()
        return total
