# Generated by Django 5.1.5 on 2025-02-24 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0019_alter_vehicle_vin'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='testdata',
            name='additional_info',
        ),
        migrations.RemoveField(
            model_name='testdata',
            name='humidity',
        ),
        migrations.RemoveField(
            model_name='testdata',
            name='pressure',
        ),
        migrations.RemoveField(
            model_name='testdata',
            name='temperature',
        ),
        migrations.AddField(
            model_name='testdata',
            name='humidity_indoor',
            field=models.FloatField(blank=True, null=True, verbose_name='Относительная влажность воздуха в помещении'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='humidity_indoor_open',
            field=models.FloatField(blank=True, null=True, verbose_name='Относительная влажность воздуха в помещении с открытыми воротами'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='humidity_road',
            field=models.FloatField(blank=True, null=True, verbose_name='Относительная влажность воздуха при проведении испытаний на дороге'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='pressure_indoor',
            field=models.FloatField(blank=True, null=True, verbose_name='Атмосферное давление в помещении'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='pressure_indoor_open',
            field=models.FloatField(blank=True, null=True, verbose_name='Атмосферное давление в помещении с открытыми воротами'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='pressure_road',
            field=models.FloatField(blank=True, null=True, verbose_name='Атмосферное давление при проведении испытаний на дороге'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='temperature_indoor',
            field=models.FloatField(blank=True, null=True, verbose_name='Температура воздуха в помещении'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='temperature_indoor_open',
            field=models.FloatField(blank=True, null=True, verbose_name='Температура воздуха в помещении с открытыми воротами'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='temperature_road',
            field=models.FloatField(blank=True, null=True, verbose_name='Температура воздуха при проведении испытаний на дороге'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='tire_pressure_front_left',
            field=models.FloatField(blank=True, null=True, verbose_name='Давление в шине (переднее левое)'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='tire_pressure_front_right',
            field=models.FloatField(blank=True, null=True, verbose_name='Давление в шине (переднее правое)'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='tire_pressure_rear_left',
            field=models.FloatField(blank=True, null=True, verbose_name='Давление в шине (заднее левое)'),
        ),
        migrations.AddField(
            model_name='testdata',
            name='tire_pressure_rear_right',
            field=models.FloatField(blank=True, null=True, verbose_name='Давление в шине (заднее правое)'),
        ),
    ]
