import os
from unicodedata import name
import kafka
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
def find_topics_by_bootstrap_servers(self):
    from .models import KafkaBootstrapSevers, KafkaTopics

    for bootstrap_servers in KafkaBootstrapSevers.objects.all():
        server = bootstrap_servers.bootstrap_servers
        consumer = kafka.KafkaConsumer(bootstrap_servers=[server])
        for topic_name in consumer.topics():
            kafka_topic, created_boolean = KafkaTopics.objects.get_or_create(topic=topic_name, bootstrap_servers=bootstrap_servers)

@app.task
def create_topic(pk):
    from .models import KafkaBootstrapSevers, KafkaTopics
    new_kafka_topic_model = KafkaTopics.objects.get(pk=pk)

    admin_client = KafkaAdminClient(
        bootstrap_servers=new_kafka_topic_model.bootstrap_servers.bootstrap_servers
    )

    topic_list = []
    topic_list.append(NewTopic(name=new_kafka_topic_model.topic, num_partitions=1, replication_factor=1))
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
