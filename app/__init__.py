from flask import Flask
from config import Config

from utili.Integration2Bizagi import Integration2Bizagi as i2b

app = Flask(__name__)
app.config.from_object(Config)

bizagi=i2b(app.config["HOST"],app.config["BASE64_KEY"])
process_id=bizagi.getProcessbyName("'Patient'")
print(process_id)
from app import routes