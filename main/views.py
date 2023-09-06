from django.shortcuts import render,redirect
from . models import *
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout   




def home(request, id=None):
    user_Profile=profile.objects.filter(user=request.user).first()
    user_expense=expense.objects.filter(user=request.user).order_by('-id')
    if request.method=="GET":
        st=request.GET.get('search')
        if st!=None:
            user_expense=expense.objects.filter(category_name=st)
    total=0
    for exp in user_expense:
         total += exp.amount
         print("here is the total exp",exp)            

    income=user_income.objects.filter(user=request.user).order_by('-id')

    return render(request,'home.html', context={'profile':user_Profile,'expense':user_expense,'income':income })

def add(request):
    user_profile=profile.objects.filter(user=request.user).first()
    USER_INCOME=user_income.objects.all()[::-1]
    category_namee=Category.objects.filter(user=request.user)
    payment_mode=Paymentmode.objects.all()

    if request.method=="POST":
        cat_id=request.POST.get('cat_name')
        cat_name = Category.objects.get(id=cat_id)
        amount=request.POST.get('amount')
        mode_id=request.POST.get('pay_mode')
        mode_type=Paymentmode.objects.get(id=mode_id)
        person=request.POST.get('person')
        transaction_type=request.POST.get('transaction_type')
        income=request.POST.get('income_hidden')



        if transaction_type == "RECIEVED":
            user_profile.balance += float(amount)
        else:         
            if user_profile.balance > float(amount):
                user_profile.expenses += float(amount)
                user_profile.balance -= float(amount)   

            else:
                messages.info(request,'insufficient balance')
                return redirect("/add/")
        if user_profile.balance  == 0:
            if request.method == 'POST':
                amount = float(request.POST.get('amount',0))
                if amount > 0:
                    user_profile.balance += amount
                    user_profile.save()
                    return redirect('/home/') 
                else:    
                    messages.info(request,"oops!! your balance is less than Expenses ")
                    return redirect('/add/')  
        expenses=expense(category_name=cat_name,person=person,amount=amount,payment_mode=mode_type,transaction_type=transaction_type,user=request.user)
        expenses.save()

        user_profile.save()
        return redirect('/home/')
    contextt={"categoryy":category_namee,
    'pay_mode':payment_mode,
    
    }
    return render(request,'add_detail.html',contextt)    
def loginn(request):
 
    if request.method=="POST":
        data=request.POST
        username=data.get('username')
        password=data.get('password')
        

        if  not User.objects.filter(username=username).exists():
            messages.error(request,'invalid usernamee')
            return redirect('/login/')
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request,'invalid username')
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/home/')    
                    
    return render(request,'login.html')

def add_category_byuser(request):
    if request.method=="POST":
        category_byuser=request.POST.get('add_category')

        cat = Category.objects.create(user=request.user, name=category_byuser)
        cat.save()
        return redirect('/add/')

    return render(request,'add_detail.html')

def income(request):
    user_profile=profile.objects.filter(user=request.user).first()
    USER_INCOME=user_income.objects.all()
    extra_incomee=extra_income.objects.filter(user=request.user)

    if request.method =="POST":
   
        person=request.POST.get('person')
        Income=request.POST.get('income')
        purpose=request.POST.get('purpose')


        user_profile.balance += float(Income)

        user_profile.income += float(Income)

        U_INCOME=user_income(u_income=Income,person=person,purpose=purpose,user=request.user)
        U_INCOME.save()
        user_profile.save()
        return redirect('/home/')

    
    
    return render(request,"home.html")

def register(request):
    if request.method=="POST":
        data=request.POST
        first_name=data.get('firstname')
        last_name=data.get('lastname')
        username=data.get('username')
        password =data.get('password')
    
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request,'user already exists')
            return redirect('/login/')
        
        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            )

    
        
        user.set_password(password) 
        user.save()
        user_profile =profile.objects.create(
            user=user,
            income = 0
             )
        user_profile.save()
       
        

        messages.info(request,'account created successfully')
        return redirect('/login/') 
    
    return render(request,'login.html')
def index(request):
    return render(request,'index.html')
def new(request):
    return render(request,'new.html')

def user_logout(request):
    logout(request)
    messages.success(request,())
    return redirect('/login/')    

def update(request,id):
    update_expense=expense.objects.get(id=id)
    user_profilee=profile.objects.get(user=update_expense.user)
    payment_mode=Paymentmode.objects.all()
    all_category=Category.objects.all()
  

    if request.method=="POST":
        user_person = request.POST.get('person')
        cat_id = request.POST.get('cat_name')
        cat_name = Category.objects.get(id=cat_id)
        amount = request.POST.get('amount')
        pay_mod_id = request.POST.get('pay_mode')
        pay_mode_name = Paymentmode.objects.get(id=pay_mod_id)
        trans_type = request.POST.get('transaction_type')
        
        if update_expense.transaction_type == "RECIEVED":
            if trans_type == "RECIEVED":
                if float(user_profilee.balance) - float(update_expense.amount) + float(amount) >= 0 :
                         
                  
                        user_profilee.balance = float(user_profilee.balance) - float(update_expense.amount) + float(amount)
                      
                        user_profilee.save()
                        
                        update_expense.person = user_person
                        update_expense.category_name = cat_name
                        update_expense.amount = amount
                        update_expense.payment_mode = pay_mode_name
                        update_expense.transaction_type = trans_type
                        
                          
                        
                        update_expense.save()
                        messages.info(request, 'Transition update successfully')
                        return redirect('/home/')
                else:
                        messages.info(request, 'insufficient income')  
                        return redirect(f"/update/{update_expense.id}/")
                


            else:
                if (float(user_profilee.balance) - float(update_expense.amount)) >= float(amount):
                         
                        user_profilee.balance = float(user_profilee.balance) - float(update_expense.amount) - float(amount)
                    
                        user_profilee.expenses = float(user_profilee.expenses) + float(amount)
                        user_profilee.save()

                        update_expense.person = user_person
                        update_expense.category_name = cat_name
                        update_expense.amount = amount
                        update_expense.payment_mode = pay_mode_name
                        update_expense.transaction_type = trans_type
                        
                            
                        
                        update_expense.save()
                        messages.info(request, 'Transition update successfully')
                        return redirect('/home/')
                else:
                        messages.info(request, 'expense is too high according Balance')  
                        return redirect(f"/update/{update_expense.id}/")
            


        else:
             if trans_type == "PAYED":
                if (float(user_profilee.balance) + float(update_expense.amount)) >= float(amount)  :
                        
                        user_profilee.balance= float(user_profilee.balance) + float(update_expense.amount) - float(amount)
                        user_profilee.expenses = float(user_profilee.expenses) - float(update_expense.amount) + float(amount)
                        user_profilee.save()
       
                        update_expense.person = user_person
                        update_expense.category_name = cat_name
                        update_expense.amount = amount
                        update_expense.payment_mode = pay_mode_name
                        update_expense.transaction_type = trans_type
                          
                       
                        update_expense.save()
                        messages.info(request, 'Transition update successfully')
                        return redirect('/home/')
                else:
                        messages.info(request, 'expense is too high according Balance')  
                        return redirect(f"/update/{update_expense.id}/")
            
             else:
                
                  
                    user_profilee.balance = float(user_profilee.balance) + float(update_expense.amount) + float(amount)
                    user_profilee.expenses = float(user_profilee.expenses) - float(update_expense.amount)
                    
                    user_profilee.save()
                    
                    update_expense.person = user_person
                    update_expense.category_name = cat_name
                    update_expense.amount = amount
                    update_expense.payment_mode = pay_mode_name
                    update_expense.transaction_type = trans_type

                    update_expense.save()
                    messages.info(request, 'Transition update successfully')
                    return redirect('/home/')
    
    update_data={'updatee':user_profilee,
    'p_mode':payment_mode,
    'category':all_category,
    "update_expense": update_expense}

    return render(request,'update.html',update_data)    

def delete(request,id):
    user_expense = expense.objects.get(id=id)
    user_profilee=profile.objects.get(user=user_expense.user)

   
    if user_expense.transaction_type=="PAYED":
        user_profilee.balance = float( user_profilee.balance) + float(user_expense.amount)
        user_profilee.expenses = float(user_profilee.expenses) - float(user_expense.amount)
        user_profilee.save()
    else:
        if user_expense.amount > user_profilee.balance:
          messages.info(request,'can not delete expense , your expense will be negative ')
          return redirect('/home/')
        user_profilee.balance = float(user_profilee.balance) - float(user_expense.amount)
        user_profilee.income = float(user_profilee.income) - float(user_expense.amount)
        user_profilee.save() 

        
        
      

   
    user_expense.delete()

    return redirect('/home/')  
def indeex(request):
    return render(request,'index.html')
def income_update(request,id):
    update_query = user_income.objects.get(id=id)
    user_profilee=profile.objects.get(user=update_query.user)

    if request.method=="POST":
        update_person=request.POST.get('person')
        update_deposite=request.POST.get('amount')
        update_purpose=request.POST.get('Purpose')

        user_profilee.balance = float(user_profilee.balance) - float(update_query.u_income)
        user_profilee.income = float(user_profilee.income)- float(update_query.u_income)
      
        update_query.person = update_person
        update_query.u_income = update_deposite
        update_query.purpose = update_purpose

      
        user_profilee.balance = float(user_profilee.balance) + float(update_deposite)
        user_profilee.income = float(user_profilee.income) + float(update_deposite)

        user_profilee.save()
        update_query.save()
        return redirect('/home/')
    
    return render(request,'update_income.html',{'update_user_income':update_query}) 

def delete_income(request,id):
    user_income_profile=user_income.objects.get(id=id)
    update_profile= profile.objects.get(user=user_income_profile.user) 

   
    update_profile.balance -= float(user_income_profile.u_income)
    update_profile.income -= float(user_income_profile.u_income)

    user_income_profile.delete()
    update_profile.save()
    return redirect('/home/')
    return render(request,'home.html')