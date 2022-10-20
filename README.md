1- Clone the project (in your terminal)
``` git clone https://github.com/SodokinMarius/Django-Complete-Ecommerce-Site.git```


2- Move to project repertory
```cd  Django-Complete-Ecommerce-Site```

3- Create virtual environnment 
```virtualenv venv```

```source venv/bin/activate```

4- Install requirements 
```pip install -r requirements.txt```

5- Run and execute migrations
```python3 manage.py makemigrations```
```python3 manage.py migrate```

5- Run server
```python3 manage.py runserver```


Setup the project with Dcker

1-Start Docker engine
`sudo systemctl start docker`

2- Build dicker image
``sudo docker-compose up -d --build``


NB : Solve the error  WARNING: Retrying (Retry(total=0, connect=None, read=None, redirect=None, status=None)) after connection broken by 'SSLError(SSLEOFError(8, 'EOF occurred in violation of protocol (_ssl.c:1129)'))': /simple/asgiref/
```unset http_proxy https_proxy```

Upgrade pip 
```python3 -m pip install --upgrade pip```

