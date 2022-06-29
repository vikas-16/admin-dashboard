# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path, re_path
from apps.home import views
from .views import register_user

urlpatterns = [

    # The home page
    path('', views.index, name='home'),

    path('user-register/', register_user, name="user_register"),
    # path('login/', login_view, name="user_login"),
    # path("logout/", LogoutView.as_view(), name="logout")
    # path('logout/', user_logout, name="logout1"),
    re_path(r'^.*\.*', views.pages, name='pages'),

]
