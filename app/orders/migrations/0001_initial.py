# Generated by Django 3.1 on 2020-08-22 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('carts', '0001_initial'),
        ('payments', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateTimeField(auto_now_add=True)),
                ('ordered_date', models.DateTimeField(blank=True, null=True)),
                ('order_status', models.CharField(choices=[('I', 'In Cart'), ('O', 'Ordered'), ('F', 'Fulfilled'), ('C', 'Completed')], default='I', max_length=2)),
                ('refund_status', models.CharField(choices=[('N', 'None'), ('R', 'Requested'), ('G', 'Granted')], default='N', max_length=2)),
                ('cart_items', models.ManyToManyField(to='carts.CartItem')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='payments.payment')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
