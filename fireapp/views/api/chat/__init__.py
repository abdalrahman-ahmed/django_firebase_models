from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from fireapp.models import ChatModel
from fireapp.serializers import ChatSerializer


class CsrfExemptSessionAuthentication(SessionAuthentication):

    def enforce_csrf(self, request):
        return  # To not perform the csrf check previously happening


class ChatView(generics.ListCreateAPIView):
    """
    Chat api endpoint,
    GET: Unauthorized
    Requires headers;
    name=Authorization: Bearer --accessToken--

    Success returns dict({success: bool, chat: list([dict({id: int, message: str, ...}), ...])})
    Failure returns dict({success: bool, message: str})

    POST: Unauthorized
    Requires headers;
    name=Authorization: Bearer --accessToken--
    Requires form-data;
    name=receiver_id: str
    name=message: str

    Success returns dict({success: bool, chat: list([dict({id: int, message: str, ...}), ...])})
    Failure returns dict({success: bool, message: str})
    """

    authentication_classes = (CsrfExemptSessionAuthentication, BasicAuthentication)
    serializer_class = ChatSerializer
    permission_classes = (AllowAny,)

    unauthorized_response = {
        'success': False,
        'message': 'You don\'t have permission to access.',
    }

    @method_decorator(csrf_exempt)
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return Response(data=self.unauthorized_response, status=401)
        else:
            chat = ChatModel.get_all()
            return Response(data={'success': True, 'chat': chat})

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        self.get_serializer(data=request.data).is_valid(raise_exception=True)

        if not request.user.is_authenticated:
            return Response(data=self.unauthorized_response, status=401)
        else:
            sender_id = int(request.user.id)

            data = {field: value for field, value in request.data.items() if field != 'csrfmiddlewaretoken'}
            data.update({'sender_id': sender_id})

            ChatModel.create(data=data)

            chat = ChatModel.get_all()
            return Response(data={'success': True, 'chat': chat})
