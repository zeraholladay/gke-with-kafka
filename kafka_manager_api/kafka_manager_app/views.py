from .models import *
from rest_framework import viewsets
from rest_framework import permissions
from .serializers import *

class KafkaBootstrapSeverViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KafkaBootstrapSever.objects.all()
    serializer_class = KafkaBootstrapSeverSerializer
    permission_classes = [permissions.IsAuthenticated]

class KafkaTopicViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KafkaTopic.objects.all()
    serializer_class = KafkaTopicSerializer
    permission_classes = [permissions.IsAuthenticated]

class KafkaTopicACLViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = KafkaTopicACL.objects.all()
    serializer_class = KafkaTopicACLSerializer
    permission_classes = [permissions.IsAuthenticated]