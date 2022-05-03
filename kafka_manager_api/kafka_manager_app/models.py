from unittest import result
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.admin import ACL, ACLFilter, ResourceType, ACLOperation, ACLPermissionType, ResourcePattern
from kafka.errors import TopicAlreadyExistsError, UnknownTopicOrPartitionError

import logging
logger = logging.getLogger(__name__)

class KafkaBootstrapSever(models.Model):
    server = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.server

class KafkaTopic(models.Model):
    name = models.CharField(max_length=100)
    num_partitions = models.PositiveIntegerField(default=1)
    replication_factor = models.PositiveIntegerField(default=1)
    bootstrap_server = models.ForeignKey(KafkaBootstrapSever, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['name', 'bootstrap_server'], name='unique_name_per_bootstrap_server'),
        ]

    def __str__(self):
        return self.name

    def _get_kafka_topic(self):
        return NewTopic(name=self.name,
            num_partitions=self.num_partitions,
            replication_factor=self.replication_factor)

    def _kafka_create_topic(self):
        admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_server.server)
        try:
            result = admin_client.create_topics(new_topics=[ self._get_kafka_topic() ], validate_only=False)
        finally:
            admin_client.close()
        return result

    def _kakfa_delete_topic(self):
        admin_client = KafkaAdminClient(bootstrap_servers=self.bootstrap_server.server)
        try:
            return admin_client.delete_topics(topics=[ self.name ])
        except UnknownTopicOrPartitionError:
            logger.info(f"Topic with name '{self.name}' does not exist on server '{self.bootstrap_server.server}'")
            return None
        finally:
            admin_client.close()

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(KafkaTopic, self).save(*args, **kwargs)

    @staticmethod
    def get_or_create_no_signal(*args, **kwargs):
        try:
            return KafkaTopic.objects.get(
                **{ key: kwargs.get(key, None) for key in ('name', 'bootstrap_server') }
            )
        except KafkaTopic.DoesNotExist:
            new_kafka_topic_obj = KafkaTopic(*args, **kwargs)
            return KafkaTopic.objects.bulk_create([new_kafka_topic_obj])[0]

@receiver(pre_save, sender=KafkaTopic)
def kafka_create_topic(sender, instance, *args, **kwargs):
    instance._kafka_create_topic()

@receiver(pre_delete, sender=KafkaTopic)
def kakfa_delete_topic(sender, instance, *args, **kwargs):
    instance._kakfa_delete_topic()

class KafkaTopicACL(models.Model):
    class Operation(models.IntegerChoices):
        # ANY = 1,
        # ALL = 2,
        READ = 3,
        WRITE = 4,
        CREATE = 5,
        DELETE = 6,
        ALTER = 7,
        DESCRIBE = 8,
        # CLUSTER_ACTION = 9,
        DESCRIBE_CONFIGS = 10,
        ALTER_CONFIGS = 11,
        IDEMPOTENT_WRITE = 12

    class Permission(models.IntegerChoices):
        # ANY = 1,
        DENY = 2,
        ALLOW = 3

    principal = models.CharField(max_length=100)
    host = models.CharField(max_length=100)
    operation = models.IntegerField(choices=Operation.choices)
    permission = models.IntegerField(choices=Permission.choices)
    topic = models.ForeignKey(KafkaTopic, on_delete=models.CASCADE)

    def __str__(self):
        return f"""{self.principal} P is {self.Permission(self.permission).label} Operation {self.Operation(self.operation).label} From Host '{self.host}' On Topic {self.topic}"""

    def _get_kafka_operation(self):
        return ACLOperation(self.operation)

    def _get_kafka_permission(self):
        return ACLPermissionType(self.permission)

    def _get_acl(self):
        return ACL(
            principal=self.principal,
            host=self.host,
            operation=self._get_kafka_operation(),
            permission_type=self._get_kafka_permission(),
            resource_pattern=ResourcePattern(ResourceType.TOPIC, self.topic)
        )

    def _get_acl_filter(self):
        return ACLFilter(
            principal=self.principal,
            host=self.host,
            operation=self._get_kafka_operation(),
            permission_type=self._get_kafka_permission(),
            resource_pattern=ResourcePattern(ResourceType.TOPIC, self.topic)
        )

    def _kakfa_create_acl(self):
        admin_client = KafkaAdminClient(bootstrap_servers=self.topic.bootstrap_server.server)
        try:
            return admin_client.create_acls([self._get_acl()])
        finally:
            admin_client.close()

    def _kafka_delete_acl(self):
        admin_client = KafkaAdminClient(bootstrap_servers=self.topic.bootstrap_server.server)
        try:
            return admin_client.delete_acls([self._get_acl_filter()])
        finally:
            admin_client.close()

    def save(self, *args, **kwargs):
        if self.pk is None:
            super(KafkaTopicACL, self).save(*args, **kwargs)

@receiver(pre_save, sender=KafkaTopicACL)
def create_acl(sender, instance, *args, **kwargs):
    instance._kakfa_create_acl() #XXX: FIX ME

@receiver(pre_delete, sender=KafkaTopicACL)
def delete_acl(sender, instance, *args, **kwargs):
    instance._kafka_delete_acl() #XXX: FIX ME
