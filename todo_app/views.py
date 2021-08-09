from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User #for adding user
from django.contrib.auth import authenticate, login, logout #authenticating the user and logging in as well as logging out user
from .models import UserDetail,Usersa


task_id = 0

def index(request):
    return render(request,"todo/index.html")


def signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        firstname = request.POST["fname"]
        lastname = request.POST["lname"]
        password = request.POST["password"]

        checkuser = User.objects.all()
        for ckuser in checkuser:
            if ckuser.username == username:
                return render(request,"todo/signup.html",{
                    "message":"Username already taken."
                }) 
        
        if username == "" or email == "" or firstname == "" or lastname == "" or password == "":
            return render(request, "todo/signup.html",{
                "message" : "Invalid inputs"
            })
            
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name = firstname,
            last_name=lastname
        )
        user.save()

        saveToDb = Usersa(username=username)
        saveToDb.save()

        return render(request,"todo/index.html")

    return render(request,"todo/signup.html")
        

def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            userCheck = Usersa.objects.all()
            for ackeck in userCheck:
                if ackeck.username == username:
                    user_id = ackeck.id
            return HttpResponseRedirect(reverse("logged", args=(user_id,)))
        else:
            return render(request, "todo/login.html",{
                "message" : "Invalid Credentials"
            })

    return render(request, "todo/login.html")


def logged_user(request,user_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    users = Usersa.objects.get(pk=user_id)
    return render(request, "todo/loggedin.html", {
        "users":users,
        "tasks":users.userinfo.all(),
        "userid":user_id
    })


def logout_view(request):
    logout(request)
    return render(request, "todo/index.html", {
        "message" : "successfully logout"
    })


def addtask(request, userid):
    users = Usersa.objects.get(pk=userid)
    task = request.POST["task"]
    saveToDb = UserDetail(user=users, task=task)
    saveToDb.save()
    
    return HttpResponseRedirect(reverse("logged",args=(userid,)))



def removetask(request, userid):
    tasks = UserDetail.objects.all()
    users = Usersa.objects.all()
    task = request.POST["task"]

    for tasksa in tasks:
        if tasksa.task == task:
            task_id = tasksa.id
            for usersa in users:
                if usersa.id == userid:
                    UserDetail.objects.filter(id=task_id).delete()
    
    return HttpResponseRedirect(reverse("logged",args=(userid,)))


    

