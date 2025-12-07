from django.contrib import admin
from .models import Course,Unit, Matricula,Resource
# Register your models here.
admin.site.register(Course)
admin.site.register(Unit)
admin.site.register(Matricula)
admin.site.register(Resource)