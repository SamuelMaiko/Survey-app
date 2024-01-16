from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Survey(models.Model):
    name=models.CharField(max_length=100)  
    
    user=models.ForeignKey(User,related_name="surveys", on_delete=models.CASCADE)
    questions=models.ManyToManyField("Question",through='SurveyQuestion',related_name="surveys")
        
    class Meta:
        db_table="surveys" 
    
    def __str__(self):
        return self.name
    
    
class Question(models.Model):
    name=models.CharField(max_length=100)
    
    class Meta:
        db_table="questions" 
        
    def __str__(self):
        return self.name
    
class SurveyQuestion(models.Model):
    survey=models.ForeignKey(Survey, related_name='surveyquestion', on_delete=models.CASCADE)
    question=models.ForeignKey(Question, related_name='surveyquestion', on_delete=models.CASCADE)
    score=models.IntegerField(default=0)
    
    class Meta:
        db_table="survey_question"
        unique_together=['survey','question']
    
class Choice(models.Model):
    name=models.CharField(max_length=100)
    score=models.IntegerField()
    
    question=models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    
    class Meta:
        db_table="choices"
         
    def __str__(self):
        return self.name
    
class Response(models.Model):
    survey=models.OneToOneField(Survey, related_name="response", on_delete=models.CASCADE)
    user=models.ForeignKey(User, related_name="responses", on_delete=models.CASCADE)
    submitted_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table="responses" 
        
        
    def __str__(self):
        return f"Response {self.id}"
    
class Answer(models.Model):
    question=models.ForeignKey(Question, related_name="answers", on_delete=models.CASCADE)
    choice=models.ForeignKey(Choice, related_name="answers", on_delete=models.CASCADE)
    response=models.ForeignKey(Response, related_name="answers", on_delete=models.CASCADE)

    class Meta:
        db_table="answers" 
        unique_together=['question','response']
        
    def __str__(self):
        return f"Answer {self.id}"