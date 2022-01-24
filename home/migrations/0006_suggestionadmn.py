# Generated by Django 4.0.1 on 2022-01-19 03:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0005_alter_product_category'),
    ]

    operations = [
        migrations.CreateModel(
            name='suggestionAdmn',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('suggestion', models.CharField(max_length=300, null=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='home.customer')),
            ],
        ),
    ]