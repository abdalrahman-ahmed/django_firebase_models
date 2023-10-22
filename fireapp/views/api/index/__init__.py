from rest_framework.response import Response
from rest_framework.views import APIView


class APIRoot(APIView):
    """
    This is the base class for all api views.
    """

    def get(self, request, *args, **kwargs):
        """
        Return a list of all the existing api endpoints.
        """

        context = {
            'routes': [
                {'register': f'{request.scheme}://{request.get_host()}/api/register'},
                {'login': f'{request.scheme}://{request.get_host()}/api/login'},
                {'chat': f'{request.scheme}://{request.get_host()}/api/chat'},
            ]
        }

        return Response(context, status=200)
