from django.contrib.auth.models import AbstractUser
from django.db import models

'''
Inheriting Abstract User to create a custom user model for Sphere Connect.
This allows us to use email as the primary identifier for authentication 
instead of the default username.
'''

class User(AbstractUser):
    
    #Creating a database field for email and setting it to be unique to
    #ensure no two users can register with the same email address.
    email = models.EmailField(unique=True)

    #Setting the USERNAME_FIELD to email so that Django uses the email
    #field for authentication instead of the default username field.
    USERNAME_FIELD = "email"
    #Specifying that the username field is required for user creation,
    #even though we are using email for authentication. This is necessary
    REQUIRED_FIELDS = ["username"]

    #Overriding the __str__ method to return the email of the user when
    #the user object is printed or converted to a string. This is useful
    def __str__(self):
        return self.email