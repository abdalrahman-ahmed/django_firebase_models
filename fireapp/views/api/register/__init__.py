from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.response import Response
from fireapp.serializers import RegisterSerializer
from fireapp.models import UserModel


class RegisterView(generics.CreateAPIView):
    """
    Register api endpoint,
    GET: AllowAny

    POST:
    Requires form-data;
    name=name: str
    name=email: str
    name=phone: str
    name=password: str
    name=confirm_password: str

    Success returns dict({success: bool, access_token: str})
    Failure returns dict({success: bool, message: str})
    """

    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    default_message = 'This is the register api endpoint'
    user_exists_message = 'Register failed, User already exists'
    password_match_message = 'Register failed, Passwords do not match'

    def get(self, request): return Response(data={'message': self.default_message})

    def post(self, request, *args, **kwargs):
        self.get_serializer(data=request.data).is_valid(raise_exception=True)

        data = request.data.dict()
        password = data['password']
        confirm_password = data['confirm_password']

        # print(data)
        if password == confirm_password:
            data.pop('csrfmiddlewaretoken', None)
            data.pop('confirm_password', None)
            user = UserModel.register(data)

            if user:
                return Response(data=user)
            else:
                return Response(data={'success': False, 'message': self.user_exists_message}, status=401)
        else:
            return Response(data={'success': False, 'message': self.password_match_message}, status=400)
