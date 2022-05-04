from .models import *
from rest_framework import serializers

class KafkaClusterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaCluster
        fields = ['pk', 'bootstrap_servers']

class KafkaTopicSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaTopic
        fields = ['pk', 'name', 'num_partitions', 'replication_factor', 'cluster' ]

class KafkaTopicACLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaTopicACL
        fields = ['pk', 'principal', 'host', 'operation', 'permission', 'topic']