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
                
                            
                return redirect("sign_in")
            except Exception as e:
                form.add_error(None, f"Database error: {str(e)}")
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
            messages.success(request,"You are now logged in successfully! Check email for account activation link")
            
            
                        
            return redirect("homepage")
        else: 
            messages.error(request,"Invalid credentials")
            form=LoginForm(request.POST)
            context={
        'form':form,
    }
            return render(request,'authentication/signin.html', context)
        
        
    form= LoginForm()
    context={
        'form':form,
    }
    return render(request,'authentication/signin.html', context)
    
def signout(request):
    
    logout(request)
    return redirect("sign_in")

def custom(request):
    
    # latest_survey=request.user.surveys.last()
    
    # latest_surveyquestions=SurveyQuestion.objects.filter(survey_id=latest_survey.id).all()
    
    
    context={
    #    'username': request.user.username,
    #    'surveyquestion':latest_surveyquestions,
    }
    
    return render(request, 'authentication/survey_results_email.html',context)


def email_results(request):
    if request.method == 'POST':
        user_email=request.POST.get('email')
        
        latest_survey=request.user.surveys.last()
    
        surveyquestions=SurveyQuestion.objects.filter(survey_id=latest_survey.id).all()
        
        message=f"Dear {request.user.username},\nHere are the results for your survey\n"
        count=1
        total=0
        for each in surveyquestions:
            msg=f"\nQuestion {count} ({each.question.name}) -- {each.score}"
            message += msg
            count+=1
            total+=each.score
        
        totalMsg=f"\n\nTotal {total}"
        message+=totalMsg
        
        signing_off="\n\nBest Regards,\nJuniour Dev,\nSamuel Maiko"
        message+=signing_off
        
        subject="ELWANEX Survey Results"
        sender=EMAIL_HOST_USER
        recipient_list=[user_email]
        context={
            
        }
        
        try:
        
            send_mail(subject, message, sender, recipient_list, fail_silently=True)
            return redirect('homepage')
            
        except:
            return HttpResponse("email results send failed")
        
        
        # context={
            
        # }
        # message=render_to_string('authentication/survey_results_email.html',context)
        
        # email=EmailMessage(subject, message, sender, recipient_list)
        # email.fail_silently=True
        # email.send()
        