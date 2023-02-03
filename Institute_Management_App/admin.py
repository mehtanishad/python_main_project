from django.contrib import admin
from .models import *

# Register your models here.
all_models = [Master, Common, Teacher, Student, Role, Club, Book, Department, Event]
for md in all_models:
    admin.site.register(md)