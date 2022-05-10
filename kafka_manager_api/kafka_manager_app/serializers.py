from .models import *
from rest_framework import serializers

class KafkaClusterSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaCluster
        fields = ['pk', 'bootstrap_servers', 'description']

class KafkaTopicSerializer(serializers.HyperlinkedModelSerializer):
    replication_factor = serializers.IntegerField(write_only=True) #make optional
    num_partitions = serializers.IntegerField(write_only=True) #make optional
    cluster = serializers.PrimaryKeyRelatedField(queryset=KafkaCluster.objects.all())

    class Meta:
        model = KafkaTopic
        fields = ['pk', 'name', 'num_partitions', 'replication_factor', 'cluster', 'description' ]

class KafkaTopicACLSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KafkaTopicACL
        fields = ['pk', 'principal', 'host', 'operation', 'permission', 'topic_id']