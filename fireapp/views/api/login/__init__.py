from rest_framework import generics
from rest_framework.response import Response
from fireapp.core.firebase import firestore, auth
from google.cloud.firestore_v1 import FieldFilter
from fireapp.serializers import LoginSerializer
from fireapp.models import UserModel


class LoginView(generics.GenericAPIView):
    """
    Login api endpoint,
    GET: AllowAny

    POST: AllowAny
    Requires form-data;
    name=email: str
    name=password: str

    Success returns dict({success: bool, access_token: str})
    Failure returns dict({success: bool, message: str})
    """

    serializer_class = LoginSerializer

    default_message = 'This is the login api endpoint'
    failure_message = 'Login failed, incorrect email or password please try again.'

    def get(self, request): return Response(data={'message': self.default_message})

    def post(self, request):
        self.get_serializer(data=request.data).is_valid(raise_exception=True)

        email = request.data['email']
        password = request.data['password']

        user = UserModel.login(email, password)

        if user:
            return Response(data=user)
        else:
            return Response(data={'success': False, 'message': self.failure_message}, status=401)
