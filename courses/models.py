#pylint:disable=E1101  
from django.db import models
from django.contrib.auth.models import User #pylint:disable=E0401
import re
# Create your models here.
class Course(models.Model):
    title = models.CharField(max_length=16,blank=False,null=False)
    description = models.CharField(max_length=100,blank=False,null=False)
    teacher = models.CharField(max_length=25,blank=True)
    # through: Especifica la tabla intermedia
    # enrolled_courses: Nombre de la relación inversa
    students = models.ManyToManyField(User, 
                                      through='Matricula',         related_name='enrolled_courses') 
    def __str__(self):
        txt = "{0:<16} : {1:<50}"
        return txt.format(self.title,self.description)

class Unit(models.Model):
    title = models.CharField(max_length=16,blank=False,null=False)
    description = models.CharField(max_length=100,blank=False,null=False)
    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name='units')
    def __str__(self):
        txt = "{0:<16} -- {1:<16}"
        return txt.format(self.title,self.course.title)  
class Matricula(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True) 
    class Meta:
        unique_together = ('student','course')
        verbose_name = 'Matricula'
        verbose_name_plural = 'Matriculas'
    def __str__(self):
        txt = "Student: {0:<12} | Course: {1:<12} | Created: {2:<12}"
        return txt.format(self.student.username,self.course.title,self.created)

class Resource(models.Model):
    # Tipos de recursos definidos como constantes (Best Practice)
    VIDEO = 'VIDEO'
    PDF = 'PDF'
    FORM = 'FORM'
    
    RESOURCE_TYPES = [
        (VIDEO, 'Video de YouTube'),
        (PDF, 'Material Descargable (PDF)'),
        (FORM, 'Simulacro (Google Form)'),
    ]

    unit = models.ForeignKey(Unit, related_name='resources', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    resource_type = models.CharField(max_length=5, choices=RESOURCE_TYPES)
    
    # Campo para Enlaces (Videos y Forms)
    link = models.URLField(blank=True, null=True, help_text="URL para YouTube o Google Forms")
    
    # Campo para Archivos (PDFs)
    # 'upload_to' organiza los archivos en carpetas por unidad
    file = models.FileField(upload_to='materials/', blank=True, null=True)
    def get_youtube_id(self):
        # Función que busca el ID en el formato watch?v= o youtu.be/
        if self.link:
            # Patrón para URL larga (watch?v=ID) o URL corta (youtu.be/ID)
            patterns = [
                r'(?:youtube\.com\/(?:[^\/]+\/.+\/|(?:v|e(?:mbed)?)\/|.*[?&]v=)|youtu\.be\/)([^"&?\/ ]{11})',
            ]
            for pattern in patterns:
                match = re.search(pattern, self.link)
                if match:
                    return match.group(1).strip()
        return None
    def __str__(self):
        return f"{self.title} ({self.unit.title})"