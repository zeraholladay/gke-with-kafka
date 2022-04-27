# Generated by Django 4.0.4 on 2022-04-27 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('kafka_manager_app', '0002_kafkatopics'),
    ]

    operations = [
        migrations.AddConstraint(
            model_name='kafkatopics',
            constraint=models.UniqueConstraint(fields=('topic', 'bootstrap_server'), name='unique_topic_per_server'),
        ),
    ]
