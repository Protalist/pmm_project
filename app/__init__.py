from flask import Flask
from config import Config

from utili.Integration2Bizagi import Integration2Bizagi as i2b

app = Flask(__name__)
app.config.from_object(Config)

bizagi=i2b(app.config["HOST"],app.config["BASE64_KEY"])
process_id=bizagi.getProcessbyName("'Patient'")

city_temp=bizagi.getEntities("5860f4c5-7adc-47aa-9e22-bbe01e2f1186")
city=[]
for ci in city_temp:
    city.append(ci["parameters"][0]['value'])

print(city)
from app import routes