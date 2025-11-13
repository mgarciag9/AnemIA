from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from apps.security.forms import ProfileUpdateForm, CustomPasswordChangeForm


@login_required
def profile_view(request):
    """Vista para ver y editar el perfil del usuario"""

    # Inicializar formularios
    profile_form = ProfileUpdateForm(instance=request.user)
    password_form = CustomPasswordChangeForm(user=request.user)

    # Formularios para actualizar perfil y contraseña
    if request.method == "POST":
        # Determinar qué formulario se envió
        if "update_profile" in request.POST:
            profile_form = ProfileUpdateForm(
                request.POST, request.FILES, instance=request.user
            )

            if profile_form.is_valid():
                profile_form.save()
                messages.success(request, "¡Perfil actualizado exitosamente!")
                return redirect("security:profile")
            else:
                messages.error(
                    request,
                    "Error al actualizar el perfil. Por favor revise los campos.",
                )

        elif "change_password" in request.POST:
            password_form = CustomPasswordChangeForm(
                user=request.user, data=request.POST
            )

            if password_form.is_valid():
                user = password_form.save()
                # Mantener la sesión activa después de cambiar contraseña
                update_session_auth_hash(request, user)
                messages.success(request, "¡Contraseña cambiada exitosamente!")
                return redirect("security:profile")
            else:
                messages.error(
                    request,
                    "Error al cambiar la contraseña. Por favor revise los campos.",
                )

    context = {
        "profile_form": profile_form,
        "password_form": password_form,
        "user": request.user,
    }

    return render(request, "security/profile/profile.html", context)
