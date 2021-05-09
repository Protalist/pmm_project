import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    BASE64_KEY="MGE3OWU5Mzg1MTc0NGY5MzA1NDczMmQwMmM0M2M0YWI2NzI4MTAzMjpmYTA3ZDRkOGRhMTE0YjFhZjI1MDYxZjcxMDE5NjIxZGI5MzFjNWU4"
    HOST="http://localhost:10024/pmm_project_hospital"