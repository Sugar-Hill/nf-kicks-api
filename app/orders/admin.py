from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['user',
                    'start_date',
                    'order_status',
                    'payment',
                    'refund_status',
                    ]
    list_display_links = [
        'user',
        'payment',
    ]
    list_filter = ['order_status',
                   'refund_status']
    search_fields = [
        'user__username',
    ]

    # actions = [make_refund_accepted]
