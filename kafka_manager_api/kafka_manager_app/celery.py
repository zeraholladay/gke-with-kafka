import os
from unicodedata import name
from kafka.errors import TopicAlreadyExistsError
from kafka.admin import KafkaAdminClient, NewTopic
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
    from .models import KafkaBootstrapSever, KafkaTopic

    for kafka_bootstrap_server in KafkaBootstrapSever.objects.all():
        admin_client = KafkaAdminClient(bootstrap_servers=kafka_bootstrap_server.server)
        topic_descriptions = [ topic for topic in admin_client.describe_topics() if topic['is_internal'] == False ]
        for topic_description in topic_descriptions:
            kafka_topic_obj, created_boolean = KafkaTopic.objects.get_or_create(name=topic_description['topic'], 
                                                                                bootstrap_server=kafka_bootstrap_server)
            if created_boolean:
                kafka_topic_obj.num_partitions = len(topic_description['partitions'])
                kafka_topic_obj.replication_factor = 1 #XXX: FIX ME!!! [ replicas for partion in topic_description['partitions'] for replicas in partion['replicas'] ] --> [0,0] or [0] (needs distinct set)
                kafka_topic_obj.save()
            else:
                pass #XXX: Add logic to validate actual description compared to model
