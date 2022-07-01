from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib import messages
from django.urls import reverse
from .forms import Studentregistration
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Student
from django.contrib.auth.models import User  
from django.contrib.auth import get_user_model

User = get_user_model()
@login_required(login_url="/login/")
def index(request):
    ############ This query is for show all signup form in dasboard using count method ###########
    text = Student.objects.all() 
    stu = text.count()  ######Fisrt Method##########
    active_user = User.objects.filter(is_active=True).count()###Second Method#####
    active_test = User.objects.filter(is_active=False).count()###Second Method#####
    active = User.objects.filter(is_superuser =True).count()###Second Method#####
    staff = User.objects.filter(is_staff=True).count()###Second Method#####
    all_user = get_user_model().objects.all().count()###Second Method#####
    # print(stud,"============================stud")
    context = {'segment':'index','stud':stu,'all_user_text':all_user, 'stu':text,'active_user':active_user,'activetext':active, 'staff':staff, 'active_test':active_test}

    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))


@login_required(login_url="/login/")
def pages(request):
    context = {}
    try:

        load_template = request.path.split('/')[-1]

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        context['segment'] = load_template

        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))


def register_user(request):
    msg = None
    success = False
   
    if request.method == "POST":
        form = Studentregistration(request.POST)
       
        print(form.is_valid(),form.errors,"++++++++++++++++++++++++++=")
        print(form.is_valid(),"======================form")
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True
            messages.success(request, 'Add successfully.')
            # return render(request, 'accounts/login.html', {"form": form})
            return redirect("home")

        else:
            msg = 'Form is not valid'
    else:
        form = Studentregistration()

    return render(request, "home/forms-general.html", {"form": form, "msg": msg, "success": success})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def delete_data(request, id):
   
     pi = Student.objects.get(pk=id)
     pi.delete()
     messages.success(request, 'Delete successfully.')
     return redirect('/')


def update_data(request, id):
    pi = Student.objects.get(pk=id)
    if request.method == 'POST':
        fm = Studentregistration(request.POST,request.FILES, instance=pi)
        print(fm.is_valid(),"=============================fm.is_valid()")
        if fm.is_valid():
            messages.success(request, 'Update successfully.')
            fm.save()
           
    fm = Studentregistration(instance=pi)
    
    return render(request, 'home/update-registration-form.html', {'form':fm})