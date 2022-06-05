# Generated by Django 4.0.5 on 2022-06-05 04:46

import django.contrib.postgres.fields
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('measurement_system', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='AssociationTable',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='id')),
            ],
            options={
                'db_table': 'measurement-data"."association',
                'managed': False,
            },
        ),
        migrations.AlterModelOptions(
            name='regexsettings',
            options={'verbose_name': 'RegexSetting', 'verbose_name_plural': 'RegexSettings'},
        ),
        migrations.AlterField(
            model_name='regexsettings',
            name='description',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None), size=None, verbose_name='SI description regexes'),
        ),
        migrations.AlterField(
            model_name='regexsettings',
            name='meaning',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None), size=None, verbose_name='SI meaning regexes'),
        ),
        migrations.AlterField(
            model_name='regexsettings',
            name='measurement_unit',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None), size=None, verbose_name='Measurement units regexes'),
        ),
        migrations.AlterField(
            model_name='regexsettings',
            name='type_description',
            field=django.contrib.postgres.fields.ArrayField(base_field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(), size=None), size=None, verbose_name='Type description regexes'),
        ),
    ]