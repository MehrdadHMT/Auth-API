from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from rest_framework import serializers

from task_auth.models import User, phone_regex_validator, Token


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
        extra_kwargs = {
            'phone_number': {'required': True},            
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            phone_number = validated_data['phone_number']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class TokenSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    user = UserSerializer(read_only=True)
    class Meta:
        model = Token
        fields = ['id', 'user', 'user_agent']
