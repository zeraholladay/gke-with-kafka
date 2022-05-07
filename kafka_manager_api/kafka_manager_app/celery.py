import os
from kafka.admin import KafkaAdminClient
from celery import Celery
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kafka_manager.settings')

app = Celery('kafka_manager_app')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

@app.task(bind=True)
def discover_topics(self):
    from .models import KafkaCluster, KafkaTopic

    for kafka_cluster in KafkaCluster.objects.all():
        admin_client = kafka_cluster.get_admin_client()
        kafka_cluster.description = admin_client.describe_cluster()
        kafka_cluster.save()

        topic_descriptions = [ topic for topic in admin_client.describe_topics()
            if topic['is_internal'] == False ]
        for topic_description in topic_descriptions:
            kafka_num_partitions = len(topic_description['partitions'])
            kafka_replication_factor = len(set([ replicas for partion in topic_description['partitions'] for replicas in partion['replicas'] ])) #XXX: Fix me
            KafkaTopic.get_or_create_no_signal(
                name=topic_description['topic'],
                cluster=kafka_cluster,
                num_partitions=kafka_num_partitions,
                replication_factor=kafka_replication_factor,
            )
