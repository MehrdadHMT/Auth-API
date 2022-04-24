from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.core.cache import cache

from .serializers import (UserSerializer, PhoneNumberSerializer, OTPSerializer, LoginSerializer,
                          TokensListSerializer, ChangePasswordSerializer, ForgotPasswordSerializer)
from task_auth.models import User, Token
from task_auth.operators import client_code


class UserRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_serializer = UserSerializer(data=request.data)
        user_serializer.is_valid(raise_exception=True)
        account = user_serializer.save()
        account.is_active = True
        account.save()

        user_agent = str(request.user_agent)

        token = Token.objects.get_or_create(user=account, user_agent=user_agent)[0].key

        data = dict()
        data["token"] = token

        return Response(data, status=status.HTTP_200_OK)


class UserLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        try:
            account = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({"message": "Incorrect Login credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if not account.check_password(password):
            # raise ValidationError({"message": "Incorrect Login credentials"})
            return Response({"message": "Incorrect Login credentials"}, status=status.HTTP_401_UNAUTHORIZED)

        if account.is_active:
            login(request, account)

            user_agent = str(request.user_agent)
            token = Token.objects.create(user=account, user_agent=user_agent).key

            data = dict()
            data["token"] = token

            return Response(data)
        else:
            return Response('Account is not active', status=status.HTTP_400_BAD_REQUEST)


class UserLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        request.user.auth_tokens.get(key=request.auth.key).delete()

        logout(request)

        return Response(status=status.HTTP_200_OK)


class TokensListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        data = dict()
        user = request.user
        recent_token_key = request.auth.key
        user_tokens = Token.objects.filter(user=user).exclude(key=recent_token_key)

        for token in user_tokens:
            data.update({str(token.id): token.user_agent})

        return Response(data=data)


class KillTokensView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TokensListSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tokens_id = serializer.validated_data.get('token_ids')

        Token.objects.filter(id__in=tokens_id).delete()

        return Response(status=status.HTTP_200_OK)


class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        ph_number_serializer = PhoneNumberSerializer(data=request.data)
        ph_number_serializer.is_valid()
        phone_number = ph_number_serializer.validated_data.get('phone_number')
        client_code(phone_number)

        return Response(status=status.HTTP_200_OK)


class OTPValidationView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        phone_number = user.phone_number
        serializer = OTPSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        otp_code = cache.get(phone_number)
        if otp_code == serializer.validated_data.get("otp_code"):
            user.has_valid_phone_number = True
            user.save()
            return Response(status=status.HTTP_200_OK)
        else:
            msg = "The entered OTP code is invalid, or maybe expired!"

        return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if user.check_password(serializer.validated_data.get('old_pass')):
            Token.objects.filter(user=user).delete()

            user.set_password(serializer.validated_data.get('new_pass'))
            user.save()

            user_agent = str(request.user_agent)
            token = Token.objects.get_or_create(user=user, user_agent=user_agent)[0].key

            data = dict()
            data["token"] = token

            return Response(data, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Your old password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        phone_number = serializer.validated_data.get('phone_number')
        otp_code = cache.get(phone_number)
        if otp_code == serializer.validated_data.get("otp_code"):
            user = User.objects.get(phone_number=phone_number)
            user.set_password(serializer.validated_data.get('new_pass'))
            user.save()

            Token.objects.filter(user=user).delete()

            user_agent = str(request.user_agent)
            token = Token.objects.get_or_create(user=user, user_agent=user_agent)[0].key
            data = {"token": token}
            return Response(data, status=status.HTTP_200_OK)
        else:
            msg = "The entered OTP code is invalid, or maybe expired!"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)
