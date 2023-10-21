from django.utils.deprecation import MiddlewareMixin
from fireapp.core.firebase import auth
from fireapp.models import UserModel
from django.conf import settings


class FirebaseAuthenticationMiddleware(MiddlewareMixin):
    error_message = 'Invalid Token'

    def process_request(self, request):
        request.User = None
        authorization_header = str(request.META.get('HTTP_AUTHORIZATION'))
        if settings.DEBUG and not authorization_header.startswith('Bearer '):
            authorization_header = request.method == 'POST' and request.POST.get('authorization') or ""
        if authorization_header and authorization_header.startswith('Bearer '):
            token = authorization_header.split(' ')
            if len(token) > 1:
                id_token = token[1]
                try:
                    jwd = auth.verify_id_token(id_token, check_revoked=True)
                    document_id = jwd['uid']
                    user = UserModel.document(document_id).get()
                    if user.exists:
                        request.User = user.to_dict()
                except Exception as e:
                    request.error_token = {'message': self.error_message, 'detail': e}
