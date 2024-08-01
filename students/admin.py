from django.contrib import admin

# Register your models here.
from students.models import Student, Class

# Register your models here.
admin.site.register(Student)
admin.site.register(Class)