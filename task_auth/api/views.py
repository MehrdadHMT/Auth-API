from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError
from django.shortcuts import get_object_or_404

from .serializers import UserSerializer
from task_auth.models import User, Token
from task_auth.operators import client_code


class UserRegisterView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		data = {}
		user_serializer = UserSerializer(data=request.data)
		if user_serializer.is_valid():
			account = user_serializer.save()
			account.is_active = True
			account.save()

			user_agent = str(request.user_agent)
			# token_data = {
			# 	"user": user_serializer.data,
			# 	"user_agent": str(user_agent)
			# }
			# token_serializer = TokenSerializer(data=token_data)

			# if token_serializer.is_valid(raise_exception=True):
			# 	token = token_serializer.save()
			# 	data["token"] = token_serializer.data["user_agent"]
			token = Token.objects.get_or_create(user=account, user_agent=user_agent)[0].key
			data["token"] = token
		else:
			data = user_serializer.errors

		return Response(data, status=status.HTTP_200_OK)


class UserLoginView(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		print("request.data:", request.data)
		data = {}
		req_data = request.data
		username = req_data['username']
		print("username:", username)
		password = req_data['password']
		print("password:", password)

		account = get_object_or_404(User, username=username)

		if not account.check_password(password):
			# raise ValidationError({"message": "Incorrect Login credentials"})
			return Response({"message": "Incorrect Login credentials"}, status=status.HTTP_403_FORBIDDEN)

		if account.is_active:
			print("Request user:", request.user)
			print("IsAuthenticated before login:", account.is_authenticated)

			login(request, account)
			print("Is Authenticated?", account.is_authenticated)
			print("Request user:", request.user)

			user_agent = str(request.user_agent)
			token = Token.objects.create(user=account, user_agent=user_agent).key
			print("New token:", token)
			data["token"] = token

			return Response(data)
		else:
			raise ValidationError({"400": f'Account not active'})


class UserLogoutView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		# print("Token Key:", request.auth.key)
		request.user.auth_tokens.get(key=request.auth.key).delete()

		logout(request)

		return Response(status=status.HTTP_200_OK)


class TokensListView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request):
		data = {}
		user = request.user
		user_tokens = Token.objects.filter(user=user)

		for token in user_tokens:
			data.update({str(token.id): token.user_agent})

		return Response(data=data)


class KillTokens(APIView):
	permission_classes = [IsAuthenticated]

	def post(self, request):
		tokens_id = request.data['token_ids']

		try:
			Token.objects.filter(id__in=tokens_id).delete()
		except BaseException as e:
			raise ValidationError({"400": f'{str(e)}'})

		return Response(status=status.HTTP_200_OK)


class SendOTP(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		# phone_number = str(request.user.phone_number)
		phone_number = request.data.get('phone_number')
		client_code(phone_number)

		return Response(status=status.HTTP_200_OK)


class OTPValidation(APIView):
	permission_classes = [AllowAny]

	def post(self, request):
		data = request.data
		phone_number = data.get('phone_number')
		


# @api_view(["GET"])
# @permission_classes([AllowAny])
# def current_user(request):
#
# 	user = request.user
# 	print("User:", user)
# 	return Response(user)
