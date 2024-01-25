# Generated by Django 4.2.6 on 2023-12-19 18:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vessel', '0006_remove_dischargeport_assigned_vessel_pod_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vessel',
            name='discharge_port',
            field=models.ManyToManyField(blank=True, to='Vessel.dischargeport'),
        ),
        migrations.AlterField(
            model_name='vessel',
            name='loading_port',
            field=models.ManyToManyField(blank=True, to='Vessel.loadingport'),
        ),
    ]
