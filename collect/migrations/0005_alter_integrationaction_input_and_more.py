# Generated by Django 4.0.5 on 2022-06-12 08:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collect', '0004_remove_integrationaction_meta_data_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='integrationaction',
            name='input',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='integrationaction',
            name='steps_data',
            field=models.JSONField(default=dict),
        ),
    ]
