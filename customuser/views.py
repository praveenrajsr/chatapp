from .models import CustomUser
from rest_framework import viewsets, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import Http404
from rest_framework import status
import json
from .serializers import UserSerializer, ChangePasswordSerializer
from rest_framework.permissions import IsAuthenticated

from customuser import serializers


class UserDetail(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return CustomUser.objects.get(pk=pk)
        except CustomUser.DoesNotExist:
            raise Http404

    def get(self, request, id):
        queryset = CustomUser.objects.get(id=id)
        serializer_class = UserSerializer(queryset, many=False)
        return Response(serializer_class.data)

    def put(self, request, id, format=None):
        user = self.get_object(id)
        data = json.loads(request.body)
        # if mobile number changed, have to check that number is already registered or not
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id, format=None):
        snippet = self.get_object(id)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = CustomUser.objects.all()
        serializer = UserSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        data = request.data
        serializer = UserSerializer(data=data)
        if (serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    model = CustomUser
    serializer_class = ChangePasswordSerializer

    def update(self, request, *args, **kwargs):
        # get user
        id = kwargs['pk']
        user_obj = CustomUser.objects.get(id=id)
        data = json.loads(request.body)[0]
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            # set_password also hashes the password that the user will get
            user_obj.set_password(data['password'])
            user_obj.save()
            return Response(serializer.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)
