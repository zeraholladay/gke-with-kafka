from .models import *
from rest_framework import serializers

class KafkaBootstrapSeverSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaBootstrapSever
        fields = ['pk', 'server']

class KafkaTopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaTopic
        fields = ['pk', 'name', 'num_partitions', 'replication_factor', 'bootstrap_server' ]

class KafkaTopicACLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaTopicACL
        fields = ['pk', 'principal', 'host', 'operation', 'permission', 'topic']