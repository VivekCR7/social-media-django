import os

secret_key = os.environ.get('SECRET_KEY')

print(type(secret_key))
