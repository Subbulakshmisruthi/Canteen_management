# Generated by Django 4.0.1 on 2022-01-21 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0009_customer_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='profile_pic',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
