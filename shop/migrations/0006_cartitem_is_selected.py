# Generated by Django 3.1.5 on 2021-04-05 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_cartitem_ordered'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='is_selected',
            field=models.BooleanField(default=False),
        ),
    ]
