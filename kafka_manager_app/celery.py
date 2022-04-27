import os
import kafka
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
    from .models import KafkaBootstrapSevers

    for boostrap_servers in KafkaBootstrapSevers.objects.all():
        server = boostrap_servers.bootstrap_servers
        consumer = kafka.KafkaConsumer(bootstrap_servers=[server])
        topics = consumer.topics()
        logger.info(topics)
