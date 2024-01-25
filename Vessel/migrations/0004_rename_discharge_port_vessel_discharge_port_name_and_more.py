# Generated by Django 4.2.6 on 2023-12-07 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vessel', '0003_dischargeport_loadingport_vesselagent_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vessel',
            old_name='discharge_port',
            new_name='discharge_port_name',
        ),
        migrations.RenameField(
            model_name='vessel',
            old_name='loading_port',
            new_name='loading_port_name',
        ),
        migrations.AlterField(
            model_name='vessel',
            name='assigned_agent',
            field=models.ManyToManyField(blank=True, null=True, to='Vessel.vesselagent'),
        ),
    ]