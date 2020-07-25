from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models

# Create your models here.
class Area(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.id

    def __str__(self):
        return self.name

class UserManager(models.Manager):
    def validator(self, postData):
        errors = ""
        if( len(postData['username'])<5 or len(postData['username'])>25):
             errors += "<li>Username must be 5-25 characters long, and not contain numbers.</li>"

        if( len(postData['password'])<5 or len(postData['password'])>25 ):
            errors += "<li>Password must be 5-25 characters long.</li>"

        try:
            validate_email(postData['email'])
        except ValidationError:
            errors += "<li>Enter a valid e-mail.</li>"

        # if( ((postData['phone'])[:2]!="69" or (postData['phone'])[:2]!="21" or (postData['phone'])[:2]!="22") or len(postData['phone'])!=10 ):
        if( len(postData['phone'])!=10 ):
            errors += "<li>Phone must start with 69, 21 or 22 and be 10 digits long.</li>"

        if( postData['kind'] == 'customer'):

            if( (postData['name'].isalpha()==False) or len(postData['name'])<5 or len(postData['name'])>25 ):
                errors += "<li>Write your name from 5 to 25 characters and don't put numbers in it</li>"

            if( (postData['surname'].isalpha()==False) or len(postData['surname'])<5 or len(postData['surname'])>25 ):
                errors += "<li>Write your surname from 5 to 25 characters, and don't put numbers in it!</li>"

        if( postData['kind'] == 'barbershop'):

            if( len(postData['address'])>25 ):
                errors += "<li>Write your address with no more than 25 characters</li>"

        return errors

class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=25)
    password = models.CharField(max_length=25)
    email = models.EmailField()
    phone = models.CharField(max_length=10)
    um = UserManager()

    class Meta:
        abstract = True

class Customer(User):
    name = models.CharField(max_length=25)
    surname = models.CharField(max_length=25)
    # image = models.ImageField(upload_to='customer-image', blank=True)

class Barbershop(User):
    address = models.CharField(max_length=20)
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='barber-image', blank=True)
