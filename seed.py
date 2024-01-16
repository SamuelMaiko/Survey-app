import os 
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE','myfirst.settings')
django.setup()

from survey.models import ToDoList, Item


def seed_db():
    # ToDoList.objects.create(name="Second ToDo")
    firstObj=ToDoList.objects.get(id=1)
    
    print(firstObj.item_set.all())
    
    # n=ToDoList(name="Third TodoList Same")
    # n.save()
    
    # firstObj.item_set.create(text="Coding session", complete=False)
    # print(firstObj.item_set.get(id=3))
    

if __name__=="__main__":
    seed_db()