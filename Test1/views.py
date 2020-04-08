from django.shortcuts import render
from Test1.models import testModel

from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics

from Test1.serializer import Test1Serializer

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.schemas import AutoSchema


import json

class Test1LisViewSchema(AutoSchema):
    def get_manual_fields(self,path,method):
        extra_fields = []
        if method.lower() in ('post','get'):
            extra_fields = [
                coreapi.Field('nombre')
            ]
        manual_fields =super().get_manual_fields(path,method)
        return manual_fields + extra_fields


class Test1List(APIView):
    permission_classes  = []
    esquema  =  Test1LisViewSchema ()
    def get(self, request, format=None):
        queryset = testModel.objects.filter(active=False)
        serializer = Test1Serializer(queryset, many=True)
        datas = serializer.data
        return Response(datas)
    
    def post(self, request, format=None):
        serializer = Test1Serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            datas = serializer.data
            return Response(datas)

class Test1Detail(APIView):
    permission_classes  = []
    esquema  =  Test1LisViewSchema ()
    def get_object(self, pk):
        try:
            return testModel.objects.get(pk=pk, active=False)
        except testModel.DoesNotExist:
            return "No"
    
    def get(self, request, pk, format=None):
        Id = self.get_object(pk)
        if Id != "No":
            Id = Test1Serializer(Id)
            return Response(Id.data)
        return Response("No hay Datos")
    
    def put(self, request , pk, format=None):
        Id = self.get_object(pk)
        serializer = Test1Serializer(Id, data = request.data)
        if serializer.is_valid():
            serializer.save()
            datas = serializer.data
            return Response(datas)
        return Response ("Error")

class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email,
            'date_joined': user.date_joined,
        })