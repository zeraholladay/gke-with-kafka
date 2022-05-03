from .models import *
from rest_framework import serializers


class KafkaBootstrapSeverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaBootstrapSever
        fields = ['server']

class KafkaTopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaTopic
        fields = ['name', 'num_partitions', 'replication_factor', 'bootstrap_server']

class KafkaTopicACLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaTopicACL
        fields = ['principal', 'host', 'operation', 'permission', 'topic']