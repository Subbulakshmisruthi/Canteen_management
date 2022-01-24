# Generated by Django 4.0.1 on 2022-01-18 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_order_customer_order_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('Starter', 'Starter'), ('Meal', 'Meal'), ('Dessert', 'Dessert'), ('Snack', 'Snack')], max_length=100, null=True),
        ),
    ]
