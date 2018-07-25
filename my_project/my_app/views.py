"""
Create your views here.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status  # pylint: disable=unused-import


class Sum(APIView):
    """
    Sample view class.
    """
    def post(self, request, _format=None):  # pylint: disable=unused-argument, no-self-use
        """
        Sample post request function.

        Accepts a post request with two integers
        and returns a reponse containing their sum.
        """
        int1, int2 = (int(value) for value in request.data.values())
        result = int1 + int2
        return Response(result)

