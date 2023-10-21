from django.core.validators import ValidationError
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from fireapp.models import UserModel


class RegisterSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        min_length=3,
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'text', 'placeholder': 'Name'}
    )

    email = serializers.EmailField(
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'email', 'placeholder': 'Email', 'required': 'required'}
    )

    phone = serializers.CharField(
        min_length=4,
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'text', 'placeholder': 'Phone'}
    )

    password = serializers.CharField(
        min_length=8,
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Password'}
    )

    confirm_password = serializers.CharField(
        min_length=8,
        write_only=True,
        required=True,
        # help_text='Leave empty if no change needed',
        style={'input_type': 'password', 'placeholder': 'Confirm Password'}
    )

    class Meta:
        model = UserModel
        fields = ('name', 'email', 'phone', 'password', 'confirm_password')

    def validate(self, data) -> dict:
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'Passwords do not match', 'confirm_password': 'Passwords do not match'})

        data.pop('confirm_password')
        data.update({'password': make_password(data['password'])})

        return dict(data)
