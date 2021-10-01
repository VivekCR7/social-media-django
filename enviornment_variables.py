import os

secret_key = os.environ.get('SECRET_KEY')
secret_key_1 = os.getenv('SECRET_KEY')

e = EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
em = EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')


print(e,em)
