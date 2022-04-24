from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from task_auth.models import User, phone_regex_validator
from .validators import otp_regex_validator


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(required=True, validators=[phone_regex_validator])


class OTPSerializer(serializers.Serializer):
    otp_code = serializers.CharField(required=True, validators=[otp_regex_validator])


class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(
            required=True,
            validators=[phone_regex_validator, UniqueValidator(queryset=User.objects.all())]
            )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "password", "password2", "phone_number"]

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            phone_number=validated_data['phone_number']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=20, required=True, validators=[UnicodeUsernameValidator])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])


class TokensListSerializer(serializers.Serializer):
    token_ids = serializers.ListField(child=serializers.IntegerField(), required=True, allow_empty=False)


class ChangePasswordSerializer(serializers.Serializer):
    old_pass = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_pass = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_pass_repeat = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def validate(self, attrs):
        if attrs['new_pass'] == attrs['old_pass']:
            raise serializers.ValidationError({"Same password": "New Password and old password must not be the same."})

        if attrs['new_pass'] != attrs['new_pass_repeat']:
            raise serializers.ValidationError({"Confirmation error": "New Password fields didn't match."})

        return attrs


class ForgotPasswordSerializer(serializers.Serializer):
    phone_number = serializers.CharField(
        required=True,
        validators=[phone_regex_validator]
    )
    otp_code = serializers.CharField(required=True, validators=[otp_regex_validator])
    new_pass = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    new_pass_repeat = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    def validate(self, attrs):
        if attrs['new_pass'] != attrs['new_pass_repeat']:
            raise serializers.ValidationError({"password": "New Password fields didn't match."})

        return attrs
