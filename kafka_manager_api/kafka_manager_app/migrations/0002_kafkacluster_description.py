# Generated by Django 4.0.4 on 2022-05-06 21:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kafka_manager_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='kafkacluster',
            name='description',
            field=models.JSONField(null=dict),
            preserve_default=dict,
        ),
    ]
