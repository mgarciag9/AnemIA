from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.views import View
from django.views.generic import FormView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.auth import get_user_model

from apps.security.forms import (
    LoginForm,
    RegisterForm,
    PasswordResetRequestForm,
    SetNewPasswordForm,
)

User = get_user_model()


class LoginView(FormView):
    """Vista basada en clase para el inicio de sesión"""

    template_name = "security/auth/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("core:dashboard")

    def dispatch(self, request, *args, **kwargs):
        """Redirigir si el usuario ya está autenticado"""
        if request.user.is_authenticated:
            return redirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Procesar formulario válido"""
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")

        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            messages.success(
                self.request, f"¡Bienvenido {user.get_full_name() or user.email}!"
            )
            return redirect(self.success_url)
        else:
            messages.error(self.request, "Correo o contraseña incorrectos.")
            return self.form_invalid(form)

    def form_invalid(self, form):
        """Procesar formulario inválido"""
        messages.error(self.request, "Por favor, corrige los errores en el formulario.")
        return super().form_invalid(form)


class RegisterView(FormView):
    """Vista basada en clase para el registro de usuarios"""

    template_name = "security/auth/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("security:login")

    def dispatch(self, request, *args, **kwargs):
        """Redirigir si el usuario ya está autenticado"""
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Procesar formulario válido"""
        form.save()
        messages.success(self.request, "¡Registro exitoso! Por favor inicia sesión.")
        return redirect(self.success_url)

    def form_invalid(self, form):
        """Procesar formulario inválido"""
        messages.error(self.request, "Por favor, corrige los errores en el formulario.")
        return super().form_invalid(form)


class LogoutView(LoginRequiredMixin, View):
    """Vista basada en clase para cerrar sesión"""

    login_url = reverse_lazy("security:login")

    def get(self, request, *args, **kwargs):
        """Procesar cierre de sesión por GET"""
        return self.logout_user(request)

    def post(self, request, *args, **kwargs):
        """Procesar cierre de sesión por POST"""
        return self.logout_user(request)

    def logout_user(self, request):
        """Cerrar sesión del usuario"""
        logout(request)
        messages.success(request, "¡Has cerrado sesión exitosamente!")
        return redirect("security:login")


class PasswordResetRequestView(FormView):
    """Vista para solicitar restablecimiento de contraseña"""

    template_name = "security/auth/password_reset.html"
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy("security:password_reset_done")

    def dispatch(self, request, *args, **kwargs):
        """Redirigir si el usuario ya está autenticado"""
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        """Procesar formulario válido y enviar email"""
        email = form.cleaned_data.get("email")
        user = User.objects.get(email=email)

        # Generar token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construir URL de reset
        reset_url = self.request.build_absolute_uri(
            reverse_lazy(
                "security:password_reset_confirm",
                kwargs={"uidb64": uid, "token": token},
            )
        )

        # Preparar contexto para el email
        context = {
            "user": user,
            "reset_url": reset_url,
            "site_name": "Sistema de Detección de Anemia",
        }

        # Renderizar el email
        subject = "Restablecimiento de contraseña - Sistema de Detección de Anemia"
        html_message = render_to_string(
            "security/emails/password_reset_email.html", context
        )
        plain_message = f"""
Hola {user.get_full_name()},

Has solicitado restablecer tu contraseña en el Sistema de Detección de Anemia.

Para establecer una nueva contraseña, haz clic en el siguiente enlace:
{reset_url}

Este enlace es válido por 24 horas.

Si no solicitaste este cambio, puedes ignorar este correo.

Saludos,
Sistema de Detección de Anemia
        """

        # Enviar email
        try:
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[email],
                html_message=html_message,
                fail_silently=False,
            )
            messages.success(
                self.request,
                "Se ha enviado un correo electrónico con las instrucciones para restablecer tu contraseña.",
            )
        except Exception as e:
            messages.error(
                self.request,
                f"Hubo un error al enviar el correo. Por favor, intenta nuevamente. Error: {str(e)}",
            )
            return self.form_invalid(form)

        return redirect(self.success_url)

    def form_invalid(self, form):
        """Procesar formulario inválido"""
        messages.error(self.request, "Por favor, corrige los errores en el formulario.")
        return super().form_invalid(form)


class PasswordResetDoneView(View):
    """Vista de confirmación de envío de email"""

    template_name = "security/auth/password_reset_done.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        return render(request, self.template_name)


class PasswordResetConfirmView(FormView):
    """Vista para confirmar y establecer nueva contraseña"""

    template_name = "security/auth/password_reset_confirm.html"
    form_class = SetNewPasswordForm
    success_url = reverse_lazy("security:password_reset_complete")

    def dispatch(self, request, *args, **kwargs):
        """Validar token antes de mostrar formulario"""
        if request.user.is_authenticated:
            return redirect("core:dashboard")

        # Obtener uid y token de la URL
        uidb64 = kwargs.get("uidb64")
        token = kwargs.get("token")

        try:
            # Validar y decodificar uid
            if uidb64 is None:
                raise ValueError("uidb64 es None")
            uid_bytes = urlsafe_base64_decode(uidb64)
            uid = force_str(uid_bytes)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Validar token
        if user is not None and default_token_generator.check_token(user, token):
            # Token válido, guardar usuario en sesión
            self.user = user
            return super().dispatch(request, *args, **kwargs)
        else:
            # Token inválido
            messages.error(
                request, "El enlace de restablecimiento es inválido o ha expirado."
            )
            return redirect("security:password_reset")

    def get_form_kwargs(self):
        """Pasar el usuario al formulario"""
        kwargs = super().get_form_kwargs()
        kwargs["user"] = self.user
        return kwargs

    def form_valid(self, form):
        """Guardar nueva contraseña"""
        form.save()
        messages.success(
            self.request,
            "¡Tu contraseña ha sido restablecida exitosamente! Ahora puedes iniciar sesión.",
        )
        return redirect(self.success_url)

    def form_invalid(self, form):
        """Procesar formulario inválido"""
        messages.error(self.request, "Por favor, corrige los errores en el formulario.")
        return super().form_invalid(form)


class PasswordResetCompleteView(View):
    """Vista de confirmación de restablecimiento exitoso"""

    template_name = "security/auth/password_reset_complete.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("core:dashboard")
        return render(request, self.template_name)
