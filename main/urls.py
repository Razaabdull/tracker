
from django.urls import path
from django.conf.urls.static import static
from django.conf  import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns 
from . views import *

urlpatterns = [
    path('',index,name='index'),
    path('home/',home,name="home"),
    path('add/',add,name='add-detail'),
    path('login/',loginn,name='login'),
    path('register/',register,name='register'),
    path('logout/',user_logout,name='logout'),
    path('income/',income,name='income'),
    path('new/',new,name='new'),
    path('add_category/',add_category_byuser,name='add_category'),
    path('delete/<int:id>/',delete,name='delete'),
    path('delete_income/<int:id>/',delete_income,name='delete_income'),
    path('update/<int:id>/',update,name='update'),
    path('income_update/<int:id>/',income_update,name='income_update'),
    path('graph/',graph,name='graph'),
   

 
 

]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    
    
    urlpatterns += staticfiles_urlpatterns()