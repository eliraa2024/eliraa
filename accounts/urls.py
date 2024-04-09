from django.urls import path

from .views import register  # , SignUpView


urlpatterns = [
    #path("signup/", SignUpView.as_view(), name="signup"),
    path("registrar/", register, name="registrar"),
]
