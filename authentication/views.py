from django.shortcuts import get_object_or_404, render,redirect, HttpResponseRedirect
from django.template.loader import render_to_string
from django.http import HttpResponse
from .forms import RegistrationForm, LoginForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from myfirst.settings import EMAIL_HOST_USER
from django.core.mail import send_mail, EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from premailer import Premailer
from django.contrib import messages
from survey.models import SurveyQuestion
from django.contrib.auth.decorators import login_required

# Create your views here.
def homepage(request): 
    
    context={
        
    }
    return render(request,'authentication/homepage.html', context)

def welcomepage(request): 
    
    context={
        
    }
    return render(request,'authentication/welcomepage.html', context)


def signup(request):
    if request.method =="POST":
        form=RegistrationForm(request.POST)
        
        if form.is_valid():
            try:
                form.save()
                received_username=request.POST['username']
                myUser=User.objects.get(username=received_username)
                myUser.is_active=False
                myUser.save()
                
                
                # subject="Maiko Company Registration" 
                subject="ELWANEX Registration"
                message=f"Hello {myUser.username},\nWelcome to ELWANEX survey. An email has been sent for your account activation.\n\nBest Regards,\nJunior Dev\nSamuel Maiko"
                sender=EMAIL_HOST_USER
                recipient_list=[myUser.email]
                
                send_mail(subject, message, sender, recipient_list, fail_silently=True)
                
                
                
                subject="ELWANEX Account Activation"
            
                domain=get_current_site(request).domain
                
                token=generate_token.make_token(myUser)
                
                uid64=urlsafe_base64_encode(force_bytes(myUser.pk))
                
                
                context={
                    'user':myUser,
                    'domain':domain,
                    'token':token,
                    'uid64':uid64,
                }
                message=render_to_string('authentication/account_activation.html',context)
                sender=EMAIL_HOST_USER
                recipient_list=[myUser.email]
                
                email=EmailMessage(subject, message, sender, recipient_list)
                email.fail_silently=True
                email.send()
                messages.success(request, "Account created successfully! Check email for activation link")
                            
                return redirect("sign_in")
            except Exception as e:
                form.add_error(None, f"Database error: {str(e)}")
                message.error(request, "Server error!")
                context={
                "form":form,
            }
                return render(request,'authentication/signup.html', context)
        
        else:
            form=RegistrationForm(request.POST)
            context={
                "form":form,
            }
            return render(request,'authentication/signup.html', context)
        
    form= RegistrationForm()
    context={
        "form":form,
    }
    return render(request,'authentication/signup.html', context)

def account_activation(request, uid64, token):
    
    user_id=force_str(urlsafe_base64_decode(uid64))
    # print(type(user_id))
    specific_user=get_object_or_404(User, pk=int(user_id))
    print(specific_user.username)
    
    if specific_user and generate_token.check_token(specific_user, token):
        specific_user.is_active=True
        specific_user.save()
        context={
            "user":specific_user            
        }
        return render(request, 'authentication/successful_activation.html', context)
    
    else:
        return HttpResponse("No user")  
    
    
def signin(request):
    if request.method=="POST":
        received_username=request.POST["username"]
        received_password=request.POST["password"]
        
        user=authenticate(username=received_username, password=received_password)
        
        if user is not None:
            login(request, user)
            messages.success(request,"You are now logged in successfully!")
            
            
                        
            return redirect("homepage")
        else: 
            messages.error(request,"Invalid credentials")
            form=LoginForm(request.POST)
            # form.add_error(None,"Enter ")
            context={
        'form':form,
    }
            return render(request,'authentication/signin.html', context)
        
        
    form= LoginForm()
    context={
        'form':form,
    }
    return render(request,'authentication/signin.html', context)
 
@login_required    
def signout(request):
    
    logout(request)
    messages.success(request, "You have logged out successfully!")
    return redirect("sign_in")

# def custom(request):
    
#     # latest_survey=request.user.surveys.last()
    
#     # latest_surveyquestions=SurveyQuestion.objects.filter(survey_id=latest_survey.id).all()
    
    
#     context={
#     #    'username': request.user.username,
#     #    'surveyquestion':latest_surveyquestions,
#     }
    
#     return render(request, 'authentication/survey_results_email.html',context)

# 
def email_results(request):
    if request.method == 'POST':
        user_email=request.POST.get('email')
        
        latest_survey=request.user.surveys.last()
    
        surveyquestions=SurveyQuestion.objects.filter(survey_id=latest_survey.id).all()
        
        message=f"Dear {request.user.username},\nHere are the results for your survey\n"
        count=1
        total=0
        for each in surveyquestions:
            msg=f"\n{count}. {each.question.name} -- [ Result: {each.score} ]"
            message += msg
            count+=1
            total+=each.score
        
        totalMsg=f"\n\nYour Total Points {total}"
        message+=totalMsg
        
        if total>=5 and total<=7:
            money_profile="Conservative"
        elif total>7 and total<11:
            money_profile="Balanced"
        elif total>10 and total<16:
            money_profile="Agressive"
        else:
            money_profile="Out of bounds"
        
        message+=f'\n\nYour FINANCIAL PROFILE is "{money_profile}"'
        
        signing_off="\n\nUnderstanding your financial profile can help guide your financial decisions. If you have any questions or would like personalized advice based on your profile, feel free to reach out.\n\nThank you again for your participation\n\nBest Regards,\nJuniour Dev,\nSamuel Maiko"
        message+=signing_off
        
        subject="ELWANEX Survey Results"
        sender=EMAIL_HOST_USER
        recipient_list=[user_email]
        context={
            
        }
        
        try:
        
            send_mail(subject, message, sender, recipient_list, fail_silently=True)
            messages.success(request,"Check email for survey results")
            return redirect('homepage')
            
        except:
            messages.error(request,"Failed to send results")
            return HttpResponse("email results send failed")
        
        
        # context={
            
        # }
        # message=render_to_string('authentication/survey_results_email.html',context)
        
        # email=EmailMessage(subject, message, sender, recipient_list)
        # email.fail_silently=True
        # email.send()
        