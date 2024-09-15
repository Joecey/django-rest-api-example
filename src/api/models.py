from django.db import models

# Create your models here.
class Transactions(models.Model):
    # Define fields for this datatype
    amount = models.FloatField()
    reason = models.CharField(max_length=100) # can't directly make a string field 
    loss = models.BooleanField() 
    
    # create string version of model for debugging
    
    # here we can define a string function. Call this with print(transaction)
    def __str__(self):
        return f"{self.reason} with amount of {self.amount}"