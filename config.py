import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    BASE64_KEY="YjE3Nzg5NjVhOTMwNWEzZjE2ODM5MzhlZTc0NWZjZTYxMGE1YzhhMDowYWM1NjAyNWI3ZDI0NTAzNjliZDhiNmU1Y2YyNGJkMjBjNTExZWE1"
    HOST="http://localhost:10024/pmm_hospital_project"