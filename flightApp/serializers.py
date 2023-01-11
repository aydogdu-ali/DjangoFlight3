from rest_framework import serializers #serializers import ettik

from .models import Flight #Flight Tablomuzu import ettik.

from .models import Reservation #Reservation Tablomuzu import ettik.

from .models import Passenger #Passenger Tablomuzu import ettik.

#Flight kısmına iat serializers
class FlightSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd"
        )

#Passenger kısmına ait serializers
class PassengerSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Passenger
        fields = "__all__"



#Rezervasyon kısmına ait serializers
class ReservationSerializer(serializers.ModelSerializer):
    passenger = PassengerSerializer(many=True) #bunu tanımlarsak passenger kısmı detaylı olarak döner

    flight = serializers.StringRelatedField() #modelde belirtilen str metondaki isimini döndürürüz.
    flight_id = serializers.IntegerField() #bunu da yazıyoruz ki crud işlemlerinde kullanmak için çünkü crud da isimle işlem yapmıyoruz.

    user = serializers.StringRelatedField() #modelde belirtilen str metondaki isimini döndürürüz. 

    class Meta:
        model = Reservation
        fields = ("id", "flight", "flight_id", "user", "passenger")


    #frontend tarafından gönderilen datayı reservation tablosuna kaydetmek için bu methodu yazdık.
    # Bizim tablomuzda sadeceuser_id ve Flight_id var buna göre ayırdık. Ayrıca passenger bilgisini deuser_id sinin içine aktardık.       
    def create(self, validated_data): #fronted tarafından gönderilen data dan
        passenger_data = validated_data.pop("passenger") #önce passengerı çıkarrtık. Çünkü Reservation tablomuzda böylr bir alan yok.
        validated_data["user_id"] = self.context["request"].user.id #biz burda reservationu yapan kişinin Id sini aldık. 
        #Biz bu methodla her zaman usera ulaşabiliriz.
        reservation = Reservation.objects.create(**validated_data) # şimdi reservation tablomuza gönderilen datayı kaydettik.
        
        for passenger in passenger_data: #yukarıda çıkardğığımız passenger tablosuna işlememiz için for döngüsü yaptık 
            pas = Passenger.objects.create(**passenger) #her bir passenger için bir satır oluşturduk
            reservation.passenger.add(pas)# her bir passengeri  model de  eklediğimiz manytomany ile eşleştirerek oluşturulan tabloya ekleyecek.
        
        reservation.save() #reservation kaydedilir.
        return reservation
            


# admin/yada kullanıcı yetkilinin bir uçuş içindeki rezervasyonları görmesi için hazırlandı.
class StaffFlightSerializer(serializers.ModelSerializer):
    
    reservation = ReservationSerializer(many=True, read_only=True) #uçuşa ait reservation ları alıyoruz. #sadece okuyoruz.
    
    class Meta:
        model = Flight
        fields = (
            "id",
            "flight_number",
            "operation_airlines",
            "departure_city",
            "arrival_city",
            "date_of_departure",
            "etd",
            "reservation",
        )
        
        