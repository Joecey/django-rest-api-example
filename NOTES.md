# Django REST API notes 
Let's figure out how to use Django to create a REST API framework 
> https://www.youtube.com/watch?v=NoLF7Dlu5mc

# FastAPI vs Flask vs Django
## FastAPI
- async support
- love using this 
- easy to spin up a REST API (and that's all about it)
- auto documentation 
- no admin - very simple
- use it with vlr.gg webscraper

## Flask 
- middle ground between the two 
- not completely out of the box - microservice structure 
- simple web apps and template
- using in my current workplace (Sep 2024) - although I am not sure why I don't use FastAPI instead 

## Django
- all the good stuff - full stack framework
- can pair with templating and React
- admin panel, db migrations, built in ORM,  auth, middleware
- e-commerce

# Diving into Django 
## Creating a new project 
1. .venv setup + activate
2. `pip install django djangorestframework`
3. django-admin startproject <projectName> (has to be camelCase)
4. `python src/manage.py runserver`
5. .gitignore .venv and .sqlite3!

>Can we call the top level folder for the project `src`?

Yes you can! - i think this is a nice convention if possible
- boiler plate generates settings, run configs, and a file to configure urls 
```python
urlpatterns = [
    path('admin/', admin.site.urls),    # This here is used to access your admin portal if required
]
```

## Creating Apps
- Apps are individaul microservices throughout the django framework
- e.g. for Facebook > user app, feed app, groups app
- `python src/manage.py startapp <appName>` > THESE NEED TO BE INSIDE SRC SO MAKE SURE YOU `cd` INTO IT!!!!
- Initialise a folder which is used to define models/migrations for sqlite database, configs, tests, views etc
- views can be defined as either returned html OR json data (like an API)
- most of the code you will be writing will be in these apps

## Defining REST Api package
```python
# src/restApiTutorial/settings.py

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework', # these need to be defined
    'api'   # define all app folders
]
```

## Defining models in app
- Each table/data type is defined by a class in `models.py`
```python
from django.db import models

# Create your models here.
class Transactions(models.Model):
    # Define fields for this datatype
    amount = models.FloatField()
    reason = models.CharField(max_length=100) # can't directly make a string field 
    
    # create string version of model for debugging
    
    # here we can define a string function. Call this with print(transaction)
    def __str__(self):
        return f"{self.reason} with amount of {self.amount}"
```
- once created, we can make migrations with `python manage.py makemigrations`
- and run with `python manage.py migrate`

- using rest_framework library - create a `serializer.py` that will tell django how to turn our models into json data
- The below is all boilerplate > get our Transactions model and process all its fields 
```python
from rest_framework  import serializers
from .models import Transactions    # import our Transaction object

# now how do we turn this into json?

class UserSerializer(serializers.ModelSerializer):
    class Meta: 
        model = Transactions
        fields = '__all__'

```

- serializers help clean and validate inputs - prevent SQL injection or any harmful logic

## Views - handling the logic
- Where the most of our code will be written
- See the `api/views.py` file for most of the imports
- define GET, POST, PUT, DELETE and create function 

```python
@api_view(['GET'])
def get_transactions(request):
    return Response(TransactionSerializer({'amount': 100.00, 'reason': "Test transaction", 'loss': True}))
    
```
- define paths in urls in app folder scope `urls.py`
- then define the parent path in the project scope `urls.py`
- e.g. `api/transactions` > api specified in parent, transactions specified in app
- when using serializers - make sure to specify `.data` at the end of the serializer class
- now navigate to `api/transactions` on local host and it works!

## Creating CRUD operations 
### POST
- serialize data and validate it matches our model
- navigate to path and type in the json data payload accordingly

```python 
@api_view(['POST'])
def create_transaction(request):
    serializer = TransactionSerializer(data=request.data)
    
    # is the data given valid?
    if serializer.is_valid():
        serializer.save()   # save to database if valid
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```
- in a function, we can specify `request.method` to link all CRUD methods to a single endpoint 

### GET with searchParams
- use `pk` to define a primary key which will be used as an identifier
```python
# Now you specify that you require a primary key here 
urlpatterns = [
    path('transactions/', get_transactions, name='get_transactions'),
    path('createTransaction/', create_transaction, name='create_transaction'),
    path('transactionDetail/<int:pk>', transaction_detail, name='transaction_detail')
]

```

### PUT
- meed to ensure that you specify the entire model object with the new change

### DELETE
- Option to delete is shown in the django dashabord
