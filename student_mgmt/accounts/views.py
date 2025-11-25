from django.shortcuts import render

# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

class HelloView(APIView):
    def get(self, request):
        return Response({"message": "Accounts API working"})
