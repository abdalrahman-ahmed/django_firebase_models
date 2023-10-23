from rest_framework.response import Response
from rest_framework.views import APIView


class ApiView(APIView):
    """
    Return a list of all the existing api endpoints.
    """

    paths = ['register', 'login', 'chat']

    def get(self, request, *args, **kwargs):
        scheme = request.scheme
        host = request.get_host()
        origin = f'{scheme}://{host}'

        routes = [{name: f'{origin}/api/{name}/'} for name in self.paths]

        context = {'routes': routes}

        return Response(context)
