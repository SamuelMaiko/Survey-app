from django.urls import path
from . import views

urlpatterns=[
    path('homepage/', views.homepage, name="home_page"),
    path('welcomepage/', views.welcomepage, name="welcome_page"),
    path('signup/', views.signup, name="sign_up"),
    path('signin/', views.signin, name="sign_in"),
    path('signout/', views.signout, name="sign_out"),
    path("email_results",views.email_results, name="email__results"),
    path("account_activation/<str:uid64>/<str:token>",views.account_activation, name="account__activation"),
    
]