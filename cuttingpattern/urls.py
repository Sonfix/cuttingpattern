from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('api/<str:func_name>', views.ApiCommand, name="api"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("cuttingpattern/<int:id>", views.show_cuttingpatttern, name="cuttingpattern"),
    path("explore", views.explore, name="explore"),
]