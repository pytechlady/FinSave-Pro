from django.db import models
from user_auth.models import User

# Create your models here.
class Saving(models.Model):
    pocket_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    currency = models.CharField(max_length=50)
    target_amount = models.DecimalField(max_digits=5, decimal_places=2)
    target_met = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.pocket_name}"
    

class Transaction(models.Model):
    pocket = models.ForeignKey(Saving, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.email} - {self.pocket.name} - {self.amount}"
    
    