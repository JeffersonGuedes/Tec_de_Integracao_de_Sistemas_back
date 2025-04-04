
import os
from django.core.wsgi import get_wsgi_application
from django.core.management import call_command
from django.db import connections
from django.db.utils import OperationalError
from django.apps import apps
from django.contrib.auth import get_user_model

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
application = get_wsgi_application()

if os.getenv('RAILWAY_ENVIRONMENT'):
    try:
        User = get_user_model()
        if not User.objects.filter(username=os.getenv('DJANGO_SUPERUSER_NAME')).exists():
            User.objects.create_superuser(
                username=os.getenv('DJANGO_SUPERUSER_NAME', 'admin'),
                email=os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@example.com'),
                password=os.getenv('DJANGO_SUPERUSER_PASSWORD')
            )
            print("Superusuário criado com sucesso!")
    except Exception as e:
        print(f"Erro ao criar superusuário: {e}")

def aplicar_migracoes():
    try:

        db_conn = connections['default']
        db_conn.ensure_connection()

        call_command('migrate')
        print("Migrações aplicadas com sucesso!")
    except OperationalError:
        print("O banco de dados não está acessível.")
    except Exception as e:
        print(f"Ocorreu um erro ao aplicar as migrações: {e}")


aplicar_migracoes()

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

application = get_wsgi_application()
