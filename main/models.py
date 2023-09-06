from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now






# Create your models here.
TYPES=(
    ('PAYED','PAYED'),
    ('RECIEVED','RECIEVED')
    )

class Category(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    class Meta:
      verbose_name = "Categorie"

class Paymentmode(models.Model):
    mode=models.CharField(max_length=50)

    def __str__(self):
        return self.mode

class user_income(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    person=models.CharField(max_length=100)
    u_income=models.FloatField()
    purpose=models.CharField(max_length=100)
    date=models.DateTimeField(default=now)

class extra_income(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    extra_amount=models.FloatField(default=0,blank=True,null=True)

    def __str__(self):
        return str(self.extra_amount)
  
   
class profile(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    income=models.FloatField()
    date=models.DateTimeField(default=now)  
    expenses=models.FloatField(default=0,blank=True,null=True)
    balance=models.FloatField(default=0,blank=True,null=True)

class expense(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    date=models.DateTimeField(auto_now_add=True, null=True, blank=True)
    person=models.CharField(max_length=100)
    category_name=models.ForeignKey(Category,on_delete=models.CASCADE)
    amount=models.FloatField()
    payment_mode=models.ForeignKey(Paymentmode,on_delete=models.CASCADE)
    transaction_type=models.CharField(null=True,max_length=100, choices=TYPES)  
  
