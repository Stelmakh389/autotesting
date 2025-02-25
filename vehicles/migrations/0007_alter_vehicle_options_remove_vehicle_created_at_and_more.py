# Generated by Django 5.1.5 on 2025-02-14 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0006_remove_vehicle_chassis_number_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vehicle',
            options={'ordering': ['-id'], 'verbose_name': 'Автомобиль', 'verbose_name_plural': 'Автомобили'},
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='customer_info_1',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='customer_info_2',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='model',
        ),
        migrations.RemoveField(
            model_name='vehicle',
            name='registration_number',
        ),
        migrations.AddField(
            model_name='vehicle',
            name='customer_infos',
            field=models.TextField(blank=True, null=True, verbose_name='Заказчиком предоставлены сведения'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='actual_address',
            field=models.TextField(blank=True, max_length=500, verbose_name='Фактический адрес заказчика'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='additional_equipment',
            field=models.TextField(blank=True, verbose_name='Дополнительное оборудование ТС'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='axis_1_weight',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Масса на ось 1 в кг'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='axis_2_weight',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Масса на ось 2 в кг'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='axis_3_weight',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Масса на ось 3 в кг'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='axis_4_weight',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Масса на ось 4 в кг'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='backup_brake_system',
            field=models.TextField(blank=True, verbose_name='Запасная тормозная система'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='cabin_description',
            field=models.TextField(blank=True, verbose_name='Описание кабины'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='cargo_space_description',
            field=models.TextField(blank=True, verbose_name='Описание загрузочного пространства'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='exhaust_system',
            field=models.TextField(blank=True, verbose_name='Система выпуска и нейтрализации отработавших газов'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='fifth_wheel_load',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Технически допустимая нагрузка на опорно-сцепное устройство в кг'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='front_suspension',
            field=models.TextField(blank=True, verbose_name='Передняя подвеска'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='front_track',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Колея передних колес в мм'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='fuel_system',
            field=models.TextField(blank=True, verbose_name='Система питания'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='height',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Габаритная высота ТС в мм'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='hybrid_description',
            field=models.TextField(blank=True, verbose_name='Описание гибридного ТС'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='ignition_system',
            field=models.TextField(blank=True, verbose_name='Система зажигания'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='legal_address',
            field=models.TextField(blank=True, max_length=500, verbose_name='Юридический адрес заказчика'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='length',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Габаритная длина ТС в мм'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='manufacture_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата выпуска'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='max_road_train_mass',
            field=models.PositiveIntegerField(blank=True, help_text='Только для категории N)', null=True, verbose_name='Технически допустимая максимальная масса автопоезда в кг'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='mileage',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Пробег в км'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='parking_brake_system',
            field=models.TextField(blank=True, verbose_name='Стояночная тормозная система'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='rear_suspension',
            field=models.TextField(blank=True, verbose_name='Задняя подвеска'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='rear_track',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Колея задних колес в мм'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='receipt_date',
            field=models.DateField(blank=True, null=True, verbose_name='Дата получения объекта'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='service_brake_system',
            field=models.TextField(blank=True, verbose_name='Рабочая тормозная система'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='trailer_mass_with_brakes',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Максимальная масса прицепа с тормозной системой в кг'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='trailer_mass_without_brakes',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Максимальная масса прицепа без тормозной системы в кг'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='vin',
            field=models.CharField(blank=True, max_length=17, unique=True, verbose_name='Идентификационный номер (VIN)'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='wheelbase',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Колесная база в мм'),
        ),
        migrations.AlterField(
            model_name='vehicle',
            name='width',
            field=models.PositiveIntegerField(blank=True, null=True, verbose_name='Габаритная ширина ТС в мм'),
        ),
    ]
