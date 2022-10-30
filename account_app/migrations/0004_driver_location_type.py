# Generated by Django 4.1.2 on 2022-10-30 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_app', '0003_alter_customer_user_alter_driver_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='location_type',
            field=models.CharField(blank=True, choices=[('1', 'Country To Country'), ('2', 'City To City'), ('3', 'Inside City')], default='1', max_length=1, null=True),
        ),
    ]
