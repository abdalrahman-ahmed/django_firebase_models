from rest_framework import generics
from rest_framework.response import Response
from fireapp.models import ChatModel
from fireapp.serializers import ChatSerializer


class ChatView(generics.CreateAPIView):
    """
    Chat api endpoint,
    GET: Unauthorized
    Requires headers;
    name=Authorization: Bearer --Token--

    Success returns dict({success: bool, chat: list([dict({id: int, message: str, ...}), ...])})
    Failure returns dict({success: bool, message: str})

    POST: PermissionDenied
    Requires headers;
    name=Authorization: Bearer --Token--
    Requires form-data;
    name=receiver_id: str
    name=message: str

    Success returns dict({success: bool, chat: list([dict({id: int, message: str, ...}), ...])})
    Failure returns dict({success: bool, message: str})
    """

    serializer_class = ChatSerializer

    unauthorized_response = {
        'success': False,
        'message': 'You don\'t have permission to access.',
    }

    def get(self, request):
        if not request.user.is_authenticated:
            return Response(data=self.unauthorized_response, status=401)
        else:
            chat = ChatModel.get_all()
            return Response(data={'success': True, 'chat': chat})

    def post(self, request, *args, **kwargs):
        self.get_serializer(data=request.data).is_valid(raise_exception=True)

        if not request.user.is_authenticated:
            return Response(data=self.unauthorized_response, status=401)
        else:
            sender_id = int(request.user.id)
            data = request.data.dict()
            data.pop('csrfmiddlewaretoken', None)
            data.pop('authorization', None)
            data.update({'sender_id': sender_id})

            ChatModel.create(data=data)

            chat = ChatModel.get_all()
            return Response(data={'success': True, 'chat': chat})
