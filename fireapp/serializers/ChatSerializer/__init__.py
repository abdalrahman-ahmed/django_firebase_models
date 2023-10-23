from rest_framework import serializers
from fireapp.models import ChatModel


class ChatSerializer(serializers.ModelSerializer):
    receiver_id = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'text', 'placeholder': 'User ID'}
    )

    message = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'text', 'placeholder': 'Message'}
    )

    class Meta:
        model = ChatModel
        fields = ('receiver_id', 'message')
