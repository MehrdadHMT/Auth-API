from rest_framework.decorators import api_view, permission_classes
# from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError

from .serializers import UserSerializer
from task_auth.models import User, Token


class UserRegisterView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, format=None):
		data = {}
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			account = serializer.save()
			account.is_active = True
			account.save()
			token = Token.objects.get_or_create(user=account)[0].key
			data["token"] = token
		else:
			data = serializer.errors

		return Response(data, status=status.HTTP_200_OK)


class UserLoginView(APIView):
	permission_classes = [AllowAny]

	def post(self, request, format=None):
		print("request.data:", request.data)
		data = {}
		req_data = request.data
		username = req_data['username']
		print("username:", username)
		password = req_data['password']
		print("password:", password)

		try:
			account = User.objects.get(username=username)
			print("Account:", account)
		except BaseException as e:
			raise ValidationError({"400": f'{str(e)}'})

		if not account.check_password(password):
			raise ValidationError({"message": "Incorrect Login credentials"})

		if account:
			if account.is_active:
				print("Request user:", request.user)
				print("IsAuthenticated before login:", account.is_authenticated)

				# try:
				# 	account.auth_token.delete()
				# 	print("Old token deleted ...")
				# except:
				# 	print("User has no auth_token!")

				login(request, account)
				print("Is Authenticated?", account.is_authenticated)
				print("Request user:", request.user)

				token = Token.objects.create(user=account).key
				print("New token:", token)
				data["token"] = token

				return Response(data)
			else:
				raise ValidationError({"400": f'Account not active'})

		else:
			raise ValidationError({"400": f'Account doesnt exist'})


class UserLogoutView(APIView):
	permission_classes = [IsAuthenticated]

	def get(self, request, format=None):
		# print("Token Key:", request.auth.key)
		request.user.auth_tokens.get(key=request.auth.key).delete()

		logout(request)

		return Response(status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([AllowAny])
def current_user(request):
	
	user = request.user	
	print("User:", user)
	return Response(user)
