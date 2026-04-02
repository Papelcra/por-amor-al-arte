import os
import django

# Configurar el entorno de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings') # <--- Cambia 'config' por el nombre de tu carpeta de settings
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Datos del admin (Cámbialos a tu gusto)
username = 'admin'
email = 'admin@por-amor-al-arte.com'
password = 'universidad123' # Pon una clave real aquí

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"Superusuario '{username}' creado exitosamente.")
else:
    print(f"El superusuario '{username}' ya existe.")