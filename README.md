# Social Media using django

In this project I tried to create a clone of `Instagram` not
exactly but added some of the basic features of authentication,
likes, comments. All this is done using django framework with some
amount of HTML/CSS and JS.

# Run locally

Clone the project
```
~ git clone git@github.com:VivekCR7/social-media-django.git
```

move to the cloned directory
```
~ cd social-media-django
```

create virtualenv and install the requirements file
```
~ virtualenv venv
~ source venv/bin/activate
(venv) ~ pip3 install -r requirements.txt
```

now create a new secret key for running the project
```
(venv) ~ python3 manage.py shell
>>> import secrets
>>> secrets.token_hex(24)
```
It will return a long secret key setup it in your enviornment variable
or just add those key in place of `SECRET_KEY` in settings.py
file and also set `DEBUG` value to **TRUE**.

create the datbase in postgresql and change the credentials in your
django-project's `settings.py` file.

```bash
  DATABASES = {
   'default': {
       'ENGINE': 'django.db.backends.postgresql_psycopg2',
       'NAME': '<your_database_name>',
       'USER': '<your_username>',
       'PASSWORD': '<your password>',
       'HOST': '',
       'PORT': '',
   }
}
```

After this run following 2 commands to work with your database.

```
(venv) ~ python3 manage.py makemigrations
(venv) ~ python3 manage.py migrate
```

Below is my database schema

![image](https://drive.google.com/uc?export=view&id=1QDiEV1wFb3wXQCQ2z2p7dCTCOQ3Xsosy)

Now for my project I have used **AWS** for storing my media files
if you want you can watch in the following video to learn to setup
the AWS with django or you can just remove all the lines related to AWS
in settings.py file

[Setup AWS](https://www.youtube.com/watch?v=kt3ZtW9MXhw&ab_channel=CoreySchafer)

For security reasons I'll suggest put all your credentials in enviornment variable
and access those in your python file.

Now I also have Mail server integration for reseting the password
that you need to setup seperately.

[SendGrid mail services](https://sendgrid.com/)

Now all things are done we just need to create super user so that we can
access the admin page

```
(venv) ~ python3 manage.py createsuperuser
```

Run the server.
```
(venv) ~ python3 manage.py runserver
```

# Author

[@Vivek Dubey](https://www.linkedin.com/in/vivek-dubey-cr7/)

[Official App](https://vivek-photogram.herokuapp.com/)