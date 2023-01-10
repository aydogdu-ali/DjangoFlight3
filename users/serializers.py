
from rest_framework import serializers

from django.contrib.auth.models import User #default user Modelini kullanıyorum

from rest_framework.validators import UniqueValidator #girilen mail adresinin uniq olmasını için import ettik.

from django.contrib.auth.password_validation import validate_password #django ile default gelen password validasyonlarını yapar.

from dj_rest_auth.serializers import TokenSerializer

class RegisterSerializers(serializers.ModelSerializer):

        #email adreside default olarak uniq değil uniq olması için serializersı değiştiriyoruz.
        email = serializers.EmailField(
        required=True,
        validators = [UniqueValidator(queryset=User.objects.all())] #burada queryset kullanıyoruz kontrol edeceği tablo tanınmalı.
        )
    
        #girilen passworları karşılaştırmak için fields leri değiştiriyoruz.
        password = serializers.CharField(
        write_only = True, #sadece oluşturma sırasında gözükür.
        required = True,
        validators = [validate_password],
        style = {"input_type" : "password"}
    )
        password2 = serializers.CharField(
        write_only = True,
        required = True,
        style = {"input_type" : "password"}
    )
    
        class Meta:
            model =User
            fields= (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'password2'
        )

    #burada password ile password2 yi eşleşmiyorsa hata döndürüyoruz.
        def validate(self, data):#data = fields içeriği objedir.
            if data['password'] != data['password2']:
                raise serializers.ValidationError(
                {
                    'message': 'Password fields did not match!'
                }
            )
        
            return data

            #kullanıcı oluşturma e database e kaydetme.
        def create(self, validated_data):
            password= validated_data.get('password') #geçerli datadan passwordu alıyoruz.
            validated_data.pop('password2') #geçerli datadan password2 yi sileriz.
            user= User.objects.create(**validated_data)#kullanıcıyı oluştururuz.
            user.set_password(password)#oluşan kullanıcıya passwordu ekleriz.
            user.save()# database e göndeririz.
            return user





# kullanıcı giriş yaptığında frontend kısmına kullanıcı bilgilerini dönüyoruz
class UserTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = User #user modelini kullanıyorum.
        fields = ("id", "first_name", "last_name", "email")
    
    
class CustomTokenSerializer(TokenSerializer): #custom Serializers yazıyoruz. Sadece get methodu var.
    user = UserTokenSerializer(read_only = True) #TokenSerializer inherit edirek user bilgisini çekiyoruz.
    
    class Meta(TokenSerializer.Meta):
        fields = ("key", "user") # geri dönüşü sadece id ve user bilgileri olur
        

#customToken Serializer yazarsak base.py ye bunu tanıtırız.
# REST_AUTH_SERIALIZERS = {
#     'TOKEN_SERIALIZER': 'users.serializers.CustomTokenSerializer',
    
# }