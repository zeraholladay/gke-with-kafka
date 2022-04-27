from django.db import models

class KafkaBootstrapSevers(models.Model):
    bootstrap_servers = models.CharField(max_length=30)
