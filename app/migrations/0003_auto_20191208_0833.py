# Generated by Django 2.2.5 on 2019-12-08 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_create_groups'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_type',
            field=models.CharField(choices=[('Credit', 'Credit Card'), ('Debit', 'Debit Card')], max_length=45),
        ),
        migrations.AlterField(
            model_name='paymentmethod',
            name='method_type',
            field=models.CharField(default='', max_length=255),
        ),
    ]
