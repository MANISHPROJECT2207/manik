from django.db import models
from django.contrib.auth.models import User
from website.models import Profile

class Donation(models.Model):
    user = models.ForeignKey(User, related_name='payments', on_delete=models.CASCADE)
    amount = models.IntegerField(default=0)
    paid = models.BooleanField(default=False)
    
    def __str__(self):
        return(f"{self.user} {self.amount} {self.paid}")