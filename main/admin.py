from django.contrib import admin
from. models import *


class profileadmin(admin.ModelAdmin):
    list_display = ['user','income','expenses','balance']


admin.site.register(profile,profileadmin)
class expensesadmin(admin.ModelAdmin):
    list_display=['user','category_name','person','amount','payment_mode','transaction_type']
admin.site.register(expense,expensesadmin)     
class categoryadmin(admin.ModelAdmin):
    list_display=['user','name']
admin.site.register(Category,categoryadmin) 
class Paymentmodeadmin(admin.ModelAdmin):
    list_display=['mode']
admin.site.register(Paymentmode,Paymentmodeadmin)
# class UserProfileadmin(admin.ModelAdmin):
#     list_display=['user',] 

# admin.site.register(UserProfile,UserProfileadmin)   
class user_incomeadmin(admin.ModelAdmin):
    list_display=['person','u_income','purpose','date'] 
admin.site.register(user_income,user_incomeadmin)  
    