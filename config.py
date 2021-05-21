import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    BASE64_KEY="MjI3NGM3YjQxZmRjYzMyNGYzMDI0OWExY2Q2MzRlOGQzM2FkYWUxOTo1Mjg1MDZhY2IxYWRlZjU3N2I5N2Q4MjhiYmZmMjNlNTc3YjJkNzY4"#"Y2M4YjViZTI2YTE0ZDQxOGVkOTk2ZWZhYjljMWIwMjJjNGZkMTcyYTowYWIzZjAwNDZlZjRkYWRjY2NlNDAwYjM1MTU3NjYyYTI4MTdkOTI4"
    HOST="http://localhost:10024/pmm_hospital_project"