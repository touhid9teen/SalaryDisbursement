from django.db.models import Q
from requests import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.models import Users
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer
from .authenticate import CustomAuthentication
from .utils import token_generator


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            try:
                validated_data = serializer.validated_data
                validated_data.pop('conform_password')
                user = Users.objects.create_user(**validated_data)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': f"User registration failed: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        try:
            user = Users.objects.get(Q(contract_number=serializer.data['email_or_phone']) | Q(email=serializer.data['email_or_phone']))
            print('user', user)
            token = token_generator(user)
            print('token', token)
            return Response({'access_token': token}, status=status.HTTP_200_OK)
        except Users.DoesNotExist:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class UserInfoView(APIView):
    authentication_classes = [CustomAuthentication]
    def get(self, request):
        try:
            user = Users.objects.get(id=request.user.id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)




