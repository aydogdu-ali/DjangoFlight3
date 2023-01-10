from django.shortcuts import render

from django.contrib.auth.models import User

from .serializers import RegisterSerializers

from rest_framework.generics import CreateAPIView


from rest_framework import status
from rest_framework.response import Response

from rest_framework.authtoken.models import Token

# concrete methodu
class RegisterAPI(CreateAPIView):
    queryset = User.objects.all() #kullanacağımız modeli tanımlıyoruz.
    serializer_class = RegisterSerializers # kullanacağımız serializers tanımlıyoruz.

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = Token.objects.get(user=user) #oluşturulan kullanıcı ile tokeı eşleştiririz
        data = serializer.data
        data["key"] = token.key # data dict içine token valuesunu ekleriz.
        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers) #datayı dönmüş oluruz.


   