from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.ReadOnlyField(source='actor.username')
    recipient = serializers.ReadOnlyField(source='recipient.username')

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'timestamp', 'is_read']
        read_only_fields = ['id', 'recipient', 'actor', 'verb', 'timestamp']
