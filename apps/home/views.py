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
from django.db.models import Count,Q
from django.contrib.auth.hashers import make_password


# User = get_user_model()
# @login_required(login_url="/login/")
# def index(request):
#     ############ This query is for show all signup form in dasboard using count method ###########
#     text = Student.objects.all() ######Fisrt Method##########
#     stu = text.count()  ######Fisrt Method##########
#     active_user = User.objects.filter(is_active=True).count()###Second Method#####
#     active_test = User.objects.filter(is_active=False).count()###Second Method#####
#     active = User.objects.filter(is_superuser =True).count()###Second Method#####
#     staff = User.objects.filter(is_staff=True).count()###Second Method#####
#     all_user = get_user_model().objects.all().count()###Second Method#####
#     # print(stud,"============================stud")
#     context = {'segment':'index','stud':stu,'all_user_text':all_user, 'stu':text,'active_user':active_user,'activetext':active, 'staff':staff, 'active_test':active_test}

#     html_template = loader.get_template('home/index.html')
#     return HttpResponse(html_template.render(context, request))


User = get_user_model()
@login_required(login_url="/login/")
def index(request):
    text = User.objects.all()
    count_stu = text.count()
    user_data =  User.objects.aggregate(
    actifs=Count('is_active', filter=Q(is_active=True)), 
    inactifs=Count('is_active', filter=Q(is_active=False)),
    issuper=Count('is_superuser', filter=Q(is_superuser=True)),
    isstaff=Count('is_staff', filter=Q(is_staff=False)) ,
    all_user = Count('pk')
    )
    name = request.POST.get('name', None)
    if name:
      text = User.objects.filter(Q(name__icontains=name) | Q(email__icontains=name) | Q(password__icontains=name)) 
    else:
        text = User.objects.all()
    context = {'segment':'index','stu':text,'count_stu':count_stu,'user_data':user_data}
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
    if request.method == "POST":
        form = Studentregistration(request.POST)
        # print(form.is_valid(),form.errors,"++++++++++++++++++++++++++=")
        # print(form.is_valid(),"======================form")
        if form.is_valid():
         
            username = form.cleaned_data.get("username")
            raw_password = make_password(form.cleaned_data.get("password"))
            newUser= User.objects.create(username=username, password=raw_password)
            newUser.is_staff=True
            newUser.save()
            
            messages.success(request, 'Add successfully.')
            # return render(request, 'accounts/login.html', {"form": form})
            return redirect("home")
        else:
            msg = 'Form is not valid'
    else:
        form = Studentregistration()
    return render(request, "home/forms-general.html", {"form": form})



# def register(request):
#     if request.method == "post":
#         register = register_form(request.post)
#         if register.is_valid():
#             register.save()
#             newUser=User(username=request.POST['username'],
#                          email=request.POST['email'],
#                          password=request.POST['password'])
#             newUser.save()
#             new_profile = profile(user=newUser,
#                           first_name=request.POST["first_name"],
#                           last_name=request.POST["last_name"])
#             new_profile.save()
#             return render(request,'users/success.html')
#     else:
#         register = register_form()
#     return render(request,'users/register.html',{"register":register})




def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')

def delete_data(request, id):
     pi = User.objects.get(pk=id)
     pi.delete()
     messages.success(request, 'Delete successfully.')
     return redirect('/')

def update_data(request, id):
    pi = User.objects.get(pk=id)
    if request.method == 'POST':
        fm = Studentregistration(request.POST,request.FILES, instance=pi)
        print(fm.is_valid(),"=============================fm.is_valid()")
        if fm.is_valid():
            messages.success(request, 'Update successfully.')
            fm.save()
    fm = Studentregistration(instance=pi)
    return render(request, 'home/update-registration-form.html', {'form':fm})