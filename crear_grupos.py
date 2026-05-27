"""
Script para crear los grupos de usuarios de SkyOps.
Ejecutar con: Get-Content crear_grupos.py | python manage.py shell
"""
from django.contrib.auth.models import Group, User

print("Creando grupos...")

# Crear grupo Operadores
operadores, creado = Group.objects.get_or_create(name="Operadores")
if creado:
    print("  Grupo 'Operadores' creado")
else:
    print("  Grupo 'Operadores' ya existe")

# Crear grupo Usuarios
usuarios, creado = Group.objects.get_or_create(name="Usuarios")
if creado:
    print("  Grupo 'Usuarios' creado")
else:
    print("  Grupo 'Usuarios' ya existe")

# Crear usuario operador de prueba
if not User.objects.filter(username="operador1").exists():
    op = User.objects.create_user(
        username="operador1",
        email="operador1@skyops.com",
        password="Operador123!",
        first_name="Carlos",
        last_name="Operador",
    )
    op.groups.add(operadores)
    print("  Usuario 'operador1' creado y asignado a Operadores")

# Crear usuario normal de prueba
if not User.objects.filter(username="usuario1").exists():
    u = User.objects.create_user(
        username="usuario1",
        email="luis.garcia@email.com",
        password="Usuario123!",
        first_name="Luis",
        last_name="García",
    )
    u.groups.add(usuarios)
    print("  Usuario 'usuario1' creado y asignado a Usuarios")

print("")
print("Grupos disponibles:")
for g in Group.objects.all():
    print(f"  - {g.name} ({g.user_set.count()} usuarios)")

print("")
print("Resumen de permisos:")
print("  Admin (is_staff=True) -> GET, POST, PUT, PATCH, DELETE en todo")
print("  Operadores            -> GET, POST, PUT, PATCH en todo (sin DELETE)")
print("  Usuarios              -> GET en vuelos/aeropuertos, solo sus reservas")