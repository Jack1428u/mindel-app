import os
import django
from django.contrib.auth import get_user_model

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mindel.settings") 
django.setup()

User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(username=username).exists():
    print(f"Creando superusuario: {username}")
    User.objects.create_superuser(username, email, password)
else:
    print("El superusuario ya existe.")