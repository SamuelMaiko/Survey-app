from django.urls import path
from django.contrib.auth import views as auth_views
from . import views as v

urlpatterns=[
    path('homepage/',v.homepage, name="home_page"),
    path('welcomepage/',v.welcomepage, name="welcome_page"),
    path('signup/',v.signup, name="sign_up"),
    path('signin/',v.signin, name="sign_in"),
    # path('login/',auth_views.LoginView.as_view(template_name='authentication/login.html'), name="login"),
    path('signout/',v.signout, name="sign_out"),
    path("email_results",v.email_results, name="email__results"),
    path("account_activation/<str:uid64>/<str:token>",v.account_activation, name="account__activation"),
    
]