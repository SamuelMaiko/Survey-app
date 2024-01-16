from django.urls import path
from . import views

urlpatterns=[
    path("",views.landing_page, name="landingpage"),
    path("home",views.home_page, name="homepage"),
    path("start_survey/",views.start_survey, name="start_survey"),
    path("questions/<int:id>",views.question, name="question"),
    path("next_question/<int:id>",views.next_question, name="next__question"),
    path("previous_question/<int:id>",views.previous_question, name="previous__question"),
    path("submit_answer/<int:id>",views.submit_answer, name="submit__answer"),
    path("complete/<str:survey_name>",views.complete, name="complete"),    
    path("last_question/",views.last_question, name="last__question"),    
]