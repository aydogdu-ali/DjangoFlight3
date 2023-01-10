
from .base import * #base.py de ne varsa import et anlamındadır.


#canlı ortamında kullanacağımız database parametreleri
#bunların valueları yine .env dosyasından okuması gerekir.
#bu yüzden bunları .env dosyasına tanıtırız.
DATABASES = {
 "default": {
 "ENGINE": "django.db.backends.postgresql_psycopg2",
 "NAME": config("SQL_DATABASE"),
 "USER": config("SQL_USER"),
 "PASSWORD": config("SQL_PASSWORD"),
 "HOST": config("SQL_HOST"),
 "PORT": config("SQL_PORT"),
 "ATOMIC_REQUESTS": True,
 }
}