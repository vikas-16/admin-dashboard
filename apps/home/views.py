from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from .forms import Studentregistration
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from .models import Student


User = get_user_model()
@login_required(login_url="/login/")
def index(request):
    ############ This query is for show all signup form in dasboard using count method ###########
    stud = Student.objects.all().count()   
    context = {'segment': 'index','stud':stud}

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
        # stud = Student.objects.all().count()
        # print(stud,'============stud')
        print(form.is_valid(),form.errors,"++++++++++++++++++++++++++=")
        print(form.is_valid(),"======================form")
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)

            msg = 'User created - please <a href="/login">login</a>.'
            success = True
       
            # return render(request, 'accounts/login.html', {"form": form})
            return redirect("login")

        else:
            msg = 'Form is not valid'
    else:
        form = Studentregistration()

    return render(request, "home/forms-general.html", {"form": form, "msg": msg, "success": success})


def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')
