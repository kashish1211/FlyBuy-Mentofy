# Generated by Django 3.1.5 on 2021-04-06 18:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_checkoutinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='billing_address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='shop.checkoutinfo'),
        ),
    ]