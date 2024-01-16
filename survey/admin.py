from django.contrib import admin
from .models import Survey, Question, Choice, Response, Answer, SurveyQuestion

# Register your models here.

admin.site.register(Survey)
admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Response)
admin.site.register(Answer)
admin.site.register(SurveyQuestion)
# admin.site.register(Favorite)

