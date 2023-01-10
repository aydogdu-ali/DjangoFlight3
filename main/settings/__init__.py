
from .base import *

env_name = config("ENV_NAME") #.env prod yazarsa base.py deki configrasyonu al + prod.py deki configurasyonu al.
                             # .env dev yazarsa base.py deki configrasyonu al + dev.py deki configurasyonu al.
if env_name == "prod":

 from .prod import *

elif env_name == "dev":

 from .dev import *