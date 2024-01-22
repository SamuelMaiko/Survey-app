from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question, Answer, Response, Survey, SurveyQuestion
from django.db.models import Q
from django.db import IntegrityError
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.

def landing_page(request):
    return redirect('sign_in') 

#
@login_required 
def home_page(request):
    
    context={
        
    }
    # return HttpResponse("Landing page")
    return render(request, 'survey/HomePage.html', {}) 
    

def start_survey(request):
    all_surveys=Survey.objects.filter(user_id=request.user.id).all()
    survey_count=len(all_surveys)
    new_survey=request.user.surveys.create(name=f"Survey {survey_count+1}")
    new_survey.save()
    
    new_response=Response.objects.create(user_id=request.user.id, survey=new_survey)
    new_response.save()
    # new_survey=Survey.objects.create(name=f"Survey {survey_count+1}")
    first_question=Question.objects.first()
    
    target_url=reverse('question', kwargs={'id':first_question.id})
    return redirect(target_url) 
# 
@login_required 
def question(request, id):
    
    try:
        specific_question=Question.objects.get(pk=id)
    except Question.DoesNotExist:
        return HttpResponse("Specific question not found")
    
    # if request.method =="POST":
    #     pass
    current_survey=request.user.surveys.last()
    current_response=current_survey.response
    specific_question_answer=current_response.answers.filter(Q(response_id=current_response.id) & Q(question_id=id))
    
    if not specific_question_answer.first():
        specific_question_answer="None"
    
    else:
        specific_question_answer=specific_question_answer.first().choice
    
    context={
        "question":specific_question,
        "answer":specific_question_answer
    }
    return render(request, 'survey/QuestionPage.html', context)
    
@login_required    
def next_question(request, id):
    next_id=id+1
    try:
        question=Question.objects.get(pk=next_id)
    except Question.DoesNotExist:
        recent_survey=request.user.responses.last()
        messages.success(request, "Survey completed successfully! Click on 'Send' to get results emailed ")
        
        target_url=reverse('complete', kwargs={'survey_name':recent_survey.survey.name})
        return redirect(target_url)
    
    target_url=reverse('question', kwargs={'id':next_id})
    return redirect(target_url)
@login_required 
def previous_question(request,id):
    previous_id=id-1
    first_question=Question.objects.first()
    try:
        question=Question.objects.get(pk=previous_id)
    except Question.DoesNotExist:
        target_url=reverse('question', kwargs={'id':first_question.id})
        return redirect(target_url)
    
    target_url=reverse('question', kwargs={'id':id-1})
    return redirect(target_url)
    
def submit_answer(request, id):
    
    if request.method == "POST":        
        choice_id=request.POST.get('user_choice')
        
        choice=Choice.objects.get(pk=choice_id)
        
        if choice_id:
            response=Response.objects.filter(user_id=request.user.id).last()
            
            try:
                survey_question=SurveyQuestion.objects.create(score=choice.score, question_id=id, survey_id=response.survey.id)
                survey_question.save()
            except IntegrityError as e:
                survey_question=SurveyQuestion.objects.filter(Q(question_id=id) & Q( survey_id=response.survey.id)).first()
                survey_question.score=Choice.objects.get(pk=request.POST.get('user_choice')).score
                survey_question.save()
            try:
                user_answer=Answer(choice_id=choice_id, question_id=id, response_id=response.id)
                user_answer.save()
            except IntegrityError as e:
                user_answer=response.answers.filter(Q(response_id=response.id) & Q(question_id=id)).last()
                user_answer.choice=Choice.objects.get(pk=request.POST.get('user_choice'))
                user_answer.save()
            messages.success(request, "Response recorded")
            target_url=reverse('next__question', kwargs={'id':id})
            return redirect(target_url)
        else:
            print("Hello ")
            return HttpResponse("No choice picked")
        # 

@login_required 
def complete(request, survey_name):
    context={
        
    }
    return render(request, 'survey/complete.html', context)
    

def last_question(request):
    last_question=Question.objects.last()
    
    target_url=reverse('question', kwargs={"id":last_question.id})
    return redirect(target_url)
        