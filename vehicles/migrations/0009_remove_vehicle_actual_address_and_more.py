# Generated by Django 5.1.5 on 2025-02-14 14:37

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0008_testdata_vehicle_test_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vehicle',
            name='actual_address',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='customer_infos',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='legal_address',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='receipt_date',
        ),
        migrations.CreateModel(
            name='СustomerData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('legal_address', models.TextField(blank=True, max_length=500, verbose_name='Юридический адрес заказчика')),
                ('actual_address', models.TextField(blank=True, max_length=500, verbose_name='Фактический адрес заказчика')),
                ('receipt_date', models.DateField(blank=True, null=True, verbose_name='Дата получения объекта')),
                ('customer_infos', models.TextField(blank=True, null=True, verbose_name='Заказчиком предоставлены сведения')),
                ('vehicle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_set', to='vehicles.vehicle')),
            ],
        ),
        migrations.AddField(
            model_name='vehicle',
            name='customerData',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vehicle_customer', to='vehicles.сustomerdata'),
        ),
    ]
