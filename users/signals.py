
from django.contrib.auth.models import User #user modelimiz
from django.db.models.signals import post_save #signali gönderecek method(decorater)
from django.dispatch import receiver # signals i yakalacak method
from rest_framework.authtoken.models import Token #token i tabloda oluşturmak için import ettim.

@receiver(post_save, sender=User) # user geldiktaen sonra işlem yap gibi post_save
def create_Token(sender, instance=None, created=False, **kwargs): #instance =user'dan gelen obje
    if created: #user create edilirse o user a ait token hemen token tablosunda işlenssin anlamındadır.
        Token.objects.create(user=instance) 
