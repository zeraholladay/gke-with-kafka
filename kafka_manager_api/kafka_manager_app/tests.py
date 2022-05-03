from uuid import uuid4
from django.test import TestCase
from django.db.utils import IntegrityError
from kafka.admin import KafkaAdminClient
from .models import *

def unique_topic_name():
    return f"test-{str(uuid4())}"

class KafkaBootstrapSeverTestCase(TestCase):
    def setUp(self):
        KafkaBootstrapSever.objects.create(server="kafka")

    def test_unique_server_must_be_unique(self):
        with self.assertRaises(IntegrityError):
            KafkaBootstrapSever.objects.create(server="kafka")

class KafkaTopicTestCase(TestCase):
    def setUp(self):
        self.topic_name = unique_topic_name()
        self.server = KafkaBootstrapSever.objects.create(server="kafka")
        self.topic = KafkaTopic.objects.create(name=self.topic_name, bootstrap_server=self.server)

    def tearDown(self) -> None:
        self.topic.delete()
        return super().tearDown()

    def test_unique_constraint(self):
        with self.assertRaises(TopicAlreadyExistsError):
            KafkaTopic.objects.create(name=self.topic_name, bootstrap_server=self.server)

    def test__get_kafka_topic(self):
        self.assertIsInstance(self.topic._get_kafka_topic(), NewTopic)

    def test__kafka_create_topic(self):
        with self.assertRaises(TopicAlreadyExistsError):
            self.topic._kafka_create_topic()

    def test_save(self):
        self.assertEqual(KafkaTopic.objects.all().count(), 1)
        with self.assertRaises(TopicAlreadyExistsError):
            KafkaTopic.objects.create(name=self.topic_name, bootstrap_server=self.server)
        self.assertEqual(KafkaTopic.objects.all().count(), 1)

    def test_get_or_create_no_signal(self):
        topic = KafkaTopic.get_or_create_no_signal(name=self.topic_name, bootstrap_server=self.server)
        self.assertEqual(topic, self.topic)
        new_topic_name = unique_topic_name()
        new_topic = KafkaTopic.get_or_create_no_signal(name=new_topic_name, bootstrap_server=self.server)
        admin_client = KafkaAdminClient(bootstrap_servers=self.server.server)
        self.assertTrue(new_topic_name not in [ topic['topic'] for topic in admin_client.describe_topics()])
        admin_client.close()
        new_topic.delete()

class KafkaTopicACLTestCase(TestCase):
    def setUp(self):
        self.topic_name = unique_topic_name()
        self.server = KafkaBootstrapSever.objects.create(server="kafka")
        self.topic = KafkaTopic.objects.create(name=self.topic_name, bootstrap_server=self.server)

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
