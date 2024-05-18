from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Creating a database to store our expense
class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=100) # Field to add name of product
    amount = models.IntegerField() # Field to add the price of the product
    category = models.CharField(max_length=100) # Field to add category
    date = models.DateField(auto_now=True) # Field to save dates


    def __str__(self) -> str:
        return self.name