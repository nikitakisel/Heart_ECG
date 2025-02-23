from rest_framework import serializers

from user.models import User


class RegisterSerializer(serializers.ModelSerializer):
    institution = serializers.CharField(required=False, allow_null=True)
    subdivision = serializers.CharField(required=False, allow_null=True)
    role = serializers.CharField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = (
            User.username.field.name,
            User.first_name.field.name,
            User.last_name.field.name,
            User.patronymic.field.name,
            User.email.field.name,
            User.password.field.name,
            User.is_staff.field.name,
            'institution',
            'subdivision',
            'role',
        )


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            User.last_name.field.name,
            User.first_name.field.name,
            User.patronymic.field.name,
            User.email.field.name,
        )
