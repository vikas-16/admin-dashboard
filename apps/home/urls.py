from django.urls import path, re_path
from apps.home import views
from .views import register_user

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('user-register/', views.register_user, name="user_register"),
    # path('login/', login_view, name="user_login"),
    # path("logout/", LogoutView.as_view(), name="logout")
    # path('logout/', user_logout, name="logout1"),
    path('delete/<int:id>/', views.delete_data, name="deletedata"),
    path('update/<int:id>/', views.update_data, name="updatedata"),
    re_path(r'^.*\.*', views.pages, name='pages'),

]
