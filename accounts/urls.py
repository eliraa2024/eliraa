from django.urls import path

from .views import SignUpView, register


urlpatterns = [
    path("signup/", SignUpView.as_view(), name="signup"),
    path("registrar/", register, name="registrar"),
]
