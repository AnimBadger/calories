from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def endpoints(request):
    data = [
        'api/calories',
        'api/calories/:caloriesId'
    ]
    return Response(data)
