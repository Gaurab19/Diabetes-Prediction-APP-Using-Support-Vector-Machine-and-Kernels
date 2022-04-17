
from dataclasses import dataclass
from re import S
from django.shortcuts import redirect, render
import pickle
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import  render, redirect
from numpy import var
from .forms import NewUserForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth import login, authenticate 
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .models import Testresult


# def Register(request):
#     sup = TblRegister.objects.all()
#     for i in sup:
#         print('***',i.username,i.isactive) 


def Home(request):
    # user = authenticate(username=username, password=password)
    user = request.user
    return render(request,'home.html',{'user':user})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful." )
            return redirect('login')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render (request=request, template_name="register.html", context={"register_form":form})

def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.") 
    return redirect("/register")

def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                print(user)
                return redirect("/home",{'user':user})
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="Login.html", context={"login_form":form})

def Pickle(request):
    template = loader.get_template('pickle.html')
    return HttpResponse(template.render())

@csrf_exempt
def diabetes_pre(request):

    template = loader.get_template('pickle.html')
    pregnancies = request.POST.get("Pregnancies")
    glucose = request.POST.get("Glucose")
    bloodpressure = request.POST.get("BloodPressure")
    skinthickness = request.POST.get("SkinThickness")
    insulin = request.POST.get("Insulin")
    BMI = request.POST.get("BMI")
    DiabetesPedigreeFunction = request.POST.get("DiabetesPedigreeFunction")
    age = request.POST.get("Age")

    diabetes_data = [
        [pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age]]
    diabetes_model = pickle.load(open('../diabetes_model.pickle', 'rb'))
    prediction = diabetes_model.predict(
        [[pregnancies, glucose, bloodpressure, skinthickness, insulin, BMI, DiabetesPedigreeFunction, age]])
    outcome = prediction 
    
    if outcome == 1:
        result = "Diabetic"
        data12="Diabetic"
    elif outcome == 0:
        result = "Not Diabetic"
        data12="Not Diabetic"
    current_user = request.user
    data = Testresult(patient=current_user,pregnancies=pregnancies,glucose=glucose,bloodpressure=bloodpressure,skinthickness=skinthickness,
    insulin=insulin,bmi=BMI,diabetespedigreefunction=DiabetesPedigreeFunction,age=age,outcome=data12)
    data.save()
    return HttpResponse(template.render({'result':result,'pregnancies':pregnancies,'glucose':glucose,'bloodpressure':bloodpressure,'skinthickness':skinthickness,'insulin':insulin,'BMI':BMI,'DiabetesPedigreeFunction':DiabetesPedigreeFunction,'age':age,'user':current_user}))



