from .models import *
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *

class KafkaClusterViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows bootstrap servers to be viewed or created.
    """
    queryset = KafkaCluster.objects.all()
    serializer_class = KafkaClusterSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = [ 'get', 'post' ]

class KafkaTopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows topics to be viewed, deleted, or created.
    """
    queryset = KafkaTopic.objects.all()
    serializer_class = KafkaTopicSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = [ 'get', 'post', 'delete']


class KafkaTopicACLViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows topic ACLs to be viewed, deleted, or created.
    """
    queryset = KafkaTopicACL.objects.all()
    serializer_class = KafkaTopicACLSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = [ 'get', 'post', 'delete']
