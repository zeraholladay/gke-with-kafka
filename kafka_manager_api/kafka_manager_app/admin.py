from django.contrib import admin

from .models import *

admin.site.register(KafkaBootstrapSever)
admin.site.register(KafkaTopic)
admin.site.register(KafkaTopicACL)