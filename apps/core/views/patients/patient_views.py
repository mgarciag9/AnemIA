from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.views.generic import ListView, View
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.contrib import messages
from apps.core.models import Paciente
from apps.core.forms.patient_forms import PacienteForm


class PatientListView(LoginRequiredMixin, ListView):
    """Vista principal para listar pacientes del doctor logueado"""
    model = Paciente
    template_name = 'core/patients/patient_list.html'
    context_object_name = 'pacientes'
    paginate_by = 5
    
    def get_queryset(self):
        queryset = Paciente.objects.filter(
            doctor_responsable=self.request.user
        ).annotate(
            num_reportes=Count('reportes')
        )
        
        query = self.request.GET.get('q', '')
        if query:
            queryset = queryset.filter(
                Q(nombre__icontains=query) |
                Q(apellido__icontains=query) |
                Q(correo__icontains=query) |
                Q(id__icontains=query) |
                Q(dni__icontains=query)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class PatientDetailView(LoginRequiredMixin, View):
    """Vista para obtener detalles de un paciente (JSON para modal)"""
    
    def get(self, request, patient_id):
        paciente = get_object_or_404(
            Paciente, 
            id=patient_id, 
            doctor_responsable=request.user
        )
        
        # Construir URL de foto de perfil
        foto_url = '/static/img/profile_pics/foto_por_defecto.webp'
        if paciente.foto_perfil:
            foto_url = f'/static/img/patients/{paciente.foto_perfil}'
        
        data = {
            'id': paciente.id,
            'nombre': paciente.nombre,
            'apellido': paciente.apellido,
            'nombre_completo': paciente.nombre_completo,
            'dni': paciente.dni,
            'correo': paciente.correo,
            'sexo': paciente.get_sexo_display(),
            'ciudad': paciente.ciudad or '',
            'direccion': paciente.direccion or '',
            'fecha_registro': paciente.fecha_registro.strftime('%d-%b-%Y'),
            'foto_perfil': foto_url,
            'num_reportes': paciente.reportes.count(),
            'reportes': [
                {
                    'id': reporte.id,
                    'fecha': reporte.fecha_analisis.strftime('%d-%b-%Y'),
                    'grado': reporte.grado_palidez
                }
                for reporte in paciente.reportes.all()[:5]
            ]
        }
        
        return JsonResponse(data)


class PatientCreateView(LoginRequiredMixin, View):
    """Vista para crear un nuevo paciente"""
    
    def post(self, request):
        form = PacienteForm(request.POST, request.FILES)
        
        if form.is_valid():
            paciente = form.save(commit=False)
            
            # Generar ID automático
            ultimo_paciente = Paciente.objects.order_by('-id').first()
            if ultimo_paciente:
                try:
                    numero = int(ultimo_paciente.id.split('-')[1])
                    nuevo_numero = numero + 1
                except (IndexError, ValueError):
                    nuevo_numero = 1001
            else:
                nuevo_numero = 1001
            
            paciente.id = f"Pac-{nuevo_numero}"
            paciente.doctor_responsable = request.user
            
            # Guardar imagen si existe
            if 'foto_perfil' in request.FILES:
                import os
                from django.conf import settings
                
                foto = request.FILES['foto_perfil']
                # Crear carpeta para el paciente
                static_dir = settings.STATICFILES_DIRS[0]
                paciente_dir = os.path.join(static_dir, 'img', 'patients', paciente.id)
                
                # Crear directorio del paciente si no existe
                os.makedirs(paciente_dir, exist_ok=True)
                
                # Guardar archivo con nombre limpio
                foto_nombre = f"perfil_{foto.name}"
                foto_path = os.path.join(paciente_dir, foto_nombre)
                
                # Guardar archivo
                with open(foto_path, 'wb+') as destination:
                    for chunk in foto.chunks():
                        destination.write(chunk)
                
                # Guardar ruta relativa desde la carpeta pacientes
                paciente.foto_perfil = f"{paciente.id}/{foto_nombre}"
            
            paciente.save()
            
            # Agregar mensaje de éxito para después de la recarga
            messages.success(request, 'Paciente registrado exitosamente')
            
            return JsonResponse({
                'success': True,
                'message': 'Paciente registrado exitosamente',
                'paciente_id': paciente.id,
                'paciente': {
                    'id': paciente.id,
                    'nombre': paciente.nombre,
                    'apellido': paciente.apellido,
                    'dni': paciente.dni,
                    'correo': paciente.correo
                }
            })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)


class PatientUpdateView(LoginRequiredMixin, View):
    """Vista para actualizar un paciente existente"""
    
    def post(self, request, patient_id):
        paciente = get_object_or_404(
            Paciente, 
            id=patient_id, 
            doctor_responsable=request.user
        )
        
        # Guardar la foto actual antes de procesar el formulario
        foto_actual = paciente.foto_perfil
        
        form = PacienteForm(request.POST, request.FILES, instance=paciente)
        
        if form.is_valid():
            paciente = form.save(commit=False)
            
            # Actualizar imagen solo si se subió una nueva
            if 'foto_perfil' in request.FILES:
                import os
                from django.conf import settings
                
                foto = request.FILES['foto_perfil']
                # Crear carpeta para el paciente
                static_dir = settings.STATICFILES_DIRS[0]
                paciente_dir = os.path.join(static_dir, 'img', 'patients', paciente.id)
                
                # Crear directorio del paciente si no existe
                os.makedirs(paciente_dir, exist_ok=True)
                
                # Guardar archivo con nombre limpio
                foto_nombre = f"perfil_{foto.name}"
                foto_path = os.path.join(paciente_dir, foto_nombre)
                
                # Guardar archivo
                with open(foto_path, 'wb+') as destination:
                    for chunk in foto.chunks():
                        destination.write(chunk)
                
                # Guardar ruta relativa desde la carpeta pacientes
                paciente.foto_perfil = f"{paciente.id}/{foto_nombre}"
            else:
                # Si no se subió nueva foto, mantener la existente
                paciente.foto_perfil = foto_actual
            
            paciente.save()
            
            # Agregar mensaje de éxito para después de la recarga
            messages.success(request, 'Paciente actualizado exitosamente')
            
            return JsonResponse({
                'success': True,
                'message': 'Paciente actualizado exitosamente'
            })
        else:
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)


class PatientDeleteView(LoginRequiredMixin, View):
    """Vista para eliminar un paciente"""
    
    def post(self, request, patient_id):
        paciente = get_object_or_404(
            Paciente, 
            id=patient_id, 
            doctor_responsable=request.user
        )
        
        # Eliminar carpeta del paciente si existe
        if paciente.foto_perfil or True:  # Siempre intentar eliminar la carpeta
            import os
            import shutil
            from django.conf import settings
            
            # Usar siempre la carpeta static, no staticfiles
            static_dir = settings.STATICFILES_DIRS[0]
            paciente_dir = os.path.join(static_dir, 'img', 'patients', paciente.id)
            
            # Eliminar toda la carpeta del paciente
            if os.path.exists(paciente_dir):
                shutil.rmtree(paciente_dir)
        
        paciente.delete()
        
        return JsonResponse({
            'success': True,
            'message': 'Paciente eliminado exitosamente'
        })
    
    def delete(self, request, patient_id):
        return self.post(request, patient_id)
