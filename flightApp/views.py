from django.shortcuts import render

from rest_framework import viewsets #Modelviewset
from .serializers import FlightSerializer
from .models import Flight

from rest_framework.permissions import IsAdminUser

from .permission import IsStafforReadOnly

from .serializers import ReservationSerializer #ReservationSerializer import edildi.
from .models import Reservation # Reservation modelimiz import edildi.

from .serializers import StaffFlightSerializer

from datetime import datetime, date

#uçuşlar ile ilgili CRUD işlemlerini yapacağımız views yazdık
class FlightView(viewsets.ModelViewSet):
    queryset = Flight.objects.all()
    serializer_class = FlightSerializer
    permission_classes = [IsStafforReadOnly] #LOGİN VE ADMİN İSE CRUD DEĞİLSE GET İŞLEMİNİ YAPAR.

    
    # Yetkili kullanıcının uçuş içindeki reservastion ları görmesi için methodu overread ettik.
    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        if self.request.user.is_staff: #eğer kullanıcı admin/yetkili ise tüm uçuştaki reservationları göster.
            return StaffFlightSerializer
        return serializer #yetkili değilse sacede uçuşları gösterir.


    #kullanıcıların giriş yaptığı saaten sonraki uçuşları görmesi için method yazıyoruzm.
    def get_queryset(self):
        now = datetime.now()
        current_time = now.strftime('%H:%M:%S')
        today = date.today()
        
        if self.request.user.is_staff: #admin ise tüm zamanlara ait uçuşu gösteririr.
            return super().get_queryset()
        
        else: #kullanıcı bugünkü ve sonrası uçuşları görmesi için yazıdıpımız method.
            queryset = Flight.objects.filter(date_of_departure__gt=today) # kullanıcı girdiği güne ait uçuşları ve sonrasını görür.
            
            if Flight.objects.filter(date_of_departure=today): #kullanıcı girdiği saaten sonrasını görür
                today_qs = Flight.objects.filter(date_of_departure=today).filter(etd__gt=current_time) #etd kalkış saati. 
                #burda bugün olanlar ve kalkış saatinden büyük olanları listeler.

                queryset = queryset.union(today_qs) # 2 sini birleştiriyoruz.
            return queryset #return ediyoruz.


class ReservationView(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer

    #kullanıcının sadece kendi rezervasyonunu göstermesi için methodu overread ettik.
    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_staff: #admin ve yetkili ise tüm reservationlar görülür.
            return queryset
        return queryset.filter(user= self.request.user) # admin ya da yetkili değilse kendi reservationlarını göster.
