from django.urls import path

from . import views

urlpatterns = [
    path("", views.login, name="login"),
    path("register", views.register, name="register"),
    path("profile", views.profile, name="profile"),
    path("logout", views.sign_out, name="logout"),
    path("admin-dashboard", views.admin_dashboard, name="admin_dashboard"),
]
