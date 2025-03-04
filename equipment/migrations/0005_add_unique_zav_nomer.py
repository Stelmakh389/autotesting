from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('equipment', '0004_alter_equipment_equipment_type'),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE UNIQUE INDEX equipment_zav_nomer_unique 
            ON equipment_equipment (zav_nomer) 
            WHERE zav_nomer NOT IN ('', '-', 'б/н') AND zav_nomer IS NOT NULL;
            """,
            reverse_sql="DROP INDEX IF EXISTS equipment_zav_nomer_unique;"
        ),
    ]