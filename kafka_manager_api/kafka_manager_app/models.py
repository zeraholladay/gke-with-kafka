from django.db import models
from .celery import create_topic

class KafkaBootstrapSevers(models.Model):
    bootstrap_servers = models.CharField(max_length=30)

    def __str__(self):
        return self.bootstrap_servers

class KafkaTopics(models.Model):
    topic = models.CharField(max_length=30)
    bootstrap_servers = models.ForeignKey(KafkaBootstrapSevers, on_delete=models.CASCADE)

    def save(self):
        super().save()
        create_topic.delay(self.pk)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['topic', 'bootstrap_servers'], name='unique_topic_per_server'),
        ]

    def __str__(self):
        return self.topic