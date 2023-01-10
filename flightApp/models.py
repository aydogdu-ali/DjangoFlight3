
from django.db import models
from django.contrib.auth.models import User #User modelimizi import ettik.


#önce Uçuş Tablomuzu oluşturuyoruz.
class Flight(models.Model):
    flight_number= models.CharField(max_length=10)
    operation_airlines = models.CharField(max_length=15)
    departure_city = models.CharField(max_length=30)
    arrival_city = models.CharField(max_length=30)
    date_of_departure = models.DateField()
    etd = models.TimeField()
    #related_name anlamı sanki burda rezervation adlı bir field var anlamındadır.

    def __str__(self): #tabloda görülecek başlıklar.
        return f'{self.flight_number}-{self.departure_city}-{self.arrival_city}'


#Yolcu tablosunu oluşturuyoruz.
class Passenger(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField()
    phone_number = models.IntegerField()
    create_date = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return f'{self.first_name}{self.last_name}'


#Rezervation tablosunu oluşturuyoruz.
class Reservation(models.Model): #bir kullanıcı bir den çok kişi için rezervasyon yapabilir.
    user= models.ForeignKey(User, on_delete= models.CASCADE) #bir kullanıcı birden fazla rezervasyon oluşturabilir. Ancak her bir rezervasyonu bir kullanıcıya ait olabilir.
    passenger =models.ManyToManyField(Passenger,related_name="reservation") #manytomany de on_delete belirtilemez. Çünkü başkalarıda bulunmaktadır. #yine burda related_name ile yolcuların rezervasyonlarını görmüş olurz.
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name="reservation") #bir uçuşa birden fazla kullanıcı rezervasyon yapabilir. # related_name bir tablo ile ilişki kurmak için yazılır. Burada Fligt tablosu ile ilişki modeli oluşturduk. Hangi uçuşta hangi rezervasyonların olduğunu görürüz.


