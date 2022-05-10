from urllib import request
from uuid import uuid4
from django.test import TestCase
from django.db.utils import IntegrityError
from kafka.errors import TopicAlreadyExistsError
from .models import *

BOOTSTRAP_SERVERS = "kafka-1,kafka-2,kafka-3"

from rest_framework.test import APIClient
from django.contrib.auth.models import User

class APIClusterTestCase(TestCase):
    def setUp(self):
        self.username, self.password = "admin", "admin"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.cluster = KafkaCluster.objects.create(bootstrap_servers=BOOTSTRAP_SERVERS)
        self.client = APIClient()
        self.client.login(username=self.username, password=self.password)

    def tearDown(self):
        self.client.logout()
        return super().tearDown()

    def test_cluster_get_all(self):
        request = self.client.get(f"/api/cluster")
        self.assertEqual(request.status_code, 200)

    def test_cluster_get_one(self):
        request = self.client.get(f"/api/cluster/{self.cluster.pk}")
        self.assertEqual(request.status_code, 200)

    def test_cluster_post(self):
        request = self.client.post('/api/cluster', {'bootstrap_servers': 'kafka-1,kafka-2'}, format='json')
        self.assertEqual(request.status_code, 201)

    # def test_cluster_delete(self):
    #     request = self.client.delete(f"/api/cluster/{self.cluster.pk}")
    #     self.assertEqual(request.status_code, 200)

BOOTSTRAP_SERVERS = "kafka-1,kafka-2,kafka-3"

def unique_topic_name():
    return f"test-{str(uuid4())}"

class KafkaClusterTestCase(TestCase):
    def setUp(self):
        KafkaCluster.objects.create(bootstrap_servers=BOOTSTRAP_SERVERS)

    def test_unique_server_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            KafkaCluster.objects.create(bootstrap_servers=BOOTSTRAP_SERVERS)

class KafkaTopicTestCase(TestCase):
    def setUp(self):
        self.topic_name = unique_topic_name()
        self.cluster = KafkaCluster.objects.create(bootstrap_servers=BOOTSTRAP_SERVERS)
        self.topic = KafkaTopic.objects.create(name=self.topic_name, cluster=self.cluster, num_partitions=1, replication_factor=1)

    def tearDown(self):
        self.topic.delete()
        return super().tearDown()

    def test_unique_constraint(self):
        with self.assertRaises(TopicAlreadyExistsError):
            KafkaTopic.objects.create(name=self.topic_name, cluster=self.cluster)

    def test__get_kafka_topic(self):
        self.assertIsInstance(self.topic._get_kafka_topic(), NewTopic)

    def test__kafka_create_topic(self):
        with self.assertRaises(TopicAlreadyExistsError):
            self.topic._kafka_create_topic()

    def test_save(self):
        self.assertEqual(KafkaTopic.objects.all().count(), 1)
        with self.assertRaises(TopicAlreadyExistsError):
            KafkaTopic.objects.create(name=self.topic_name, cluster=self.cluster)
        self.assertEqual(KafkaTopic.objects.all().count(), 1)

    def test_get_or_create_no_signal(self):
        topic, created_boolean = KafkaTopic.get_or_create_no_signal(name=self.topic_name, cluster=self.cluster)
        self.assertEqual(topic, self.topic)
        new_topic_name = unique_topic_name()
        new_topic, created_boolean = KafkaTopic.get_or_create_no_signal(name=new_topic_name, cluster=self.cluster)
        admin_client = self.cluster.get_admin_client()
        self.assertTrue(new_topic_name not in [ topic['topic'] for topic in admin_client.describe_topics()])
        admin_client.close()
        new_topic.delete()

class KafkaTopicACLTestCase(TestCase):
    def setUp(self):
        self.topic_name = unique_topic_name()
        self.cluster = KafkaCluster.objects.create(bootstrap_servers=BOOTSTRAP_SERVERS)
        self.topic = KafkaTopic.objects.create(name=self.topic_name, cluster=self.cluster)

    def tearDown(self) -> None:
        self.topic.delete()
        return super().tearDown()

    def test___str__(self):
        kafka_acl = KafkaTopicACL(principal="User:test",
            host="*",
            operation=KafkaTopicACL.Operation.READ,
            permission=KafkaTopicACL.Permission.ALLOW,
            topic=self.topic
        )
        self.assertEqual(str(kafka_acl), f"User:test P is Allow Operation Read From Host '*' On Topic {self.topic_name}")

    def test__get_kafka_operation(self):
        kafka_acl = KafkaTopicACL(principal="User:test",
            host="*",
            operation=KafkaTopicACL.Operation.READ,
            permission=KafkaTopicACL.Permission.ALLOW,
            topic=self.topic
        )
        self.assertIsInstance(kafka_acl._get_kafka_operation(), ACLOperation)

    def test__get_kafka_permission(self):
        kafka_acl = KafkaTopicACL(principal="User:test",
            host="*",
            operation=KafkaTopicACL.Operation.READ,
            permission=KafkaTopicACL.Permission.ALLOW,
            topic=self.topic
        )
        kafka_permission = kafka_acl._get_kafka_permission()
        self.assertIsInstance(kafka_permission, ACLPermissionType)

    def test__get_acl(self):
        kafka_acl = KafkaTopicACL(principal="User:test",
            host="*",
            operation=KafkaTopicACL.Operation.READ,
            permission=KafkaTopicACL.Permission.ALLOW,
            topic=self.topic
        )
        acl = kafka_acl._get_acl()
        self.assertIsInstance(acl, ACL)

    def test__get_acl_filter(self):
        kafka_acl = KafkaTopicACL(principal="User:test",
            host="*",
            operation=KafkaTopicACL.Operation.READ,
            permission=KafkaTopicACL.Permission.ALLOW,
            topic=self.topic
        )
        acl_filter = kafka_acl._get_acl_filter()
        self.assertIsInstance(acl_filter, ACLFilter)

    def test__kakfa_create_acl(self):
        kafka_acl = KafkaTopicACL(principal="User:test",
            host="*",
            operation=KafkaTopicACL.Operation.READ,
            permission=KafkaTopicACL.Permission.ALLOW,
            topic=self.topic
        )
        result = kafka_acl._kakfa_create_acl()
        self.assertEqual(len(result['succeeded']), 1)

    def test__kafka_delete_acl(self):
        kafka_acl = KafkaTopicACL(principal="User:test",
            host="*",
            operation=KafkaTopicACL.Operation.READ,
            permission=KafkaTopicACL.Permission.ALLOW,
            topic=self.topic
        )
        result = kafka_acl._kafka_delete_acl()
        self.assertEqual(len(result), 1)
        _, num_affected_acls, kakfa_error = result[0]
        self.assertEqual(len(num_affected_acls), 1)

    def test_save(self):
        kafka_acl_obj = KafkaTopicACL.objects.create(
            principal="User:test",
            host="*",
            operation=KafkaTopicACL.Operation.READ,
            permission=KafkaTopicACL.Permission.ALLOW,
            topic=self.topic
        )
        self.assertEqual(KafkaTopicACL.objects.all().count(), 1) #XXX: FIX ME
