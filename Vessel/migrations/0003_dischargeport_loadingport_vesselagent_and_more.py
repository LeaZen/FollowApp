# Generated by Django 4.2.6 on 2023-12-07 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Vessel', '0002_vessel_vessel_schedule'),
    ]

    operations = [
        migrations.CreateModel(
            name='DischargePort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discharge_port_name', models.CharField(blank=True, max_length=50, null=True)),
                ('anchor_discharge_port', models.DateField(blank=True, null=True)),
                ('eta_discharge_port', models.DateField(blank=True, null=True)),
                ('etb_discharge_port', models.DateField(blank=True, null=True)),
                ('ata_discharge_port', models.DateField(blank=True, null=True)),
                ('atd_discharge_port', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='LoadingPort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loading_port_name', models.CharField(blank=True, max_length=50, null=True)),
                ('anchor_loading_port', models.DateField(blank=True, null=True)),
                ('eta_loading_port', models.DateField(blank=True, null=True)),
                ('etb_loading_port', models.DateField(blank=True, null=True)),
                ('ata_loading_port', models.DateField(blank=True, null=True)),
                ('atb_loading_port', models.DateField(blank=True, null=True)),
                ('etd_loading_port', models.DateField(blank=True, null=True)),
                ('atd_loading_port', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VesselAgent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vessel_agent_name', models.CharField(blank=True, max_length=50, null=True)),
                ('vessel_agent_pic', models.CharField(blank=True, max_length=50, null=True)),
                ('vessel_agent_phone', models.IntegerField(blank=True, null=True)),
                ('vessel_agent_address', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='anchor_loading_port',
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='ata_loading_port',
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='atb_loading_port',
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='atd_loading_port',
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='eta_discharge_port',
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='eta_loading_port',
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='etb_loading_port',
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='etd_loading_port',
        ),
        migrations.AddField(
            model_name='vessel',
            name='all_dhl_received',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vessel',
            name='all_docs_received',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vessel',
            name='status_arrived',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vessel',
            name='status_complete',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vessel',
            name='status_loaded',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='vessel',
            name='status_loading',
            field=models.BooleanField(blank=True, null=True),
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='discharge_port',
        ),
        migrations.RemoveField(
            model_name='vessel',
            name='loading_port',
        ),
        migrations.AddField(
            model_name='vessel',
            name='assigned_agent',
            field=models.ManyToManyField(to='Vessel.vesselagent'),
        ),
        migrations.AddField(
            model_name='vessel',
            name='discharge_port',
            field=models.ManyToManyField(to='Vessel.dischargeport'),
        ),
        migrations.AddField(
            model_name='vessel',
            name='loading_port',
            field=models.ManyToManyField(to='Vessel.loadingport'),
        ),
    ]
