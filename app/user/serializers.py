""""
Serializers for the user API
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
)
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the user object."""

    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'name']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 6}}

    def create(self, validated_data):
        """Create and return a user with encrypted password."""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """Update and return user."""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AuthTokenSerializer(serializers.Serializer):
    """Serialize the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"},
        trim_whitespace=False
    )

    def validate(self, attrs):
        """Override the `validate` method to authenticate the user."""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(email=email, password=password)

        # Check if authentication was successful
        if user is None:
            raise serializers.ValidationError(_('Invalid email or password'))

        attrs["user"] = user
        return attrs
