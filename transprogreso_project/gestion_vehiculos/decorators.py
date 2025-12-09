from django.shortcuts import redirect
from django.contrib import messages

def rol_requerido(roles_permitidos):
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect("login")

            rol = request.user.perfil.rol

            if rol not in roles_permitidos:
                messages.error(request, "No tienes permisos para acceder a esta sección.")
                return redirect("inicio")

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
