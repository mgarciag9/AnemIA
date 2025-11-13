const modal = document.getElementById("patientModal");
const viewMode = document.getElementById("viewMode");
const formMode = document.getElementById("formMode");
const modalTitle = document.getElementById("modalTitle");
const patientForm = document.getElementById("patientForm");

// Función para obtener el token CSRF
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

const csrftoken = getCookie("csrftoken");

// ============================================
// ABRIR MODAL - VER DETALLES
// ============================================
function openModalView(patientId) {
  fetch(`/pacientes/${patientId}/`)
    .then((response) => response.json())
    .then((data) => {
      // Configurar título y modo
      modalTitle.textContent = "Detalles del Paciente";
      viewMode.style.display = "block";
      formMode.style.display = "none";

      // Llenar información
      document.getElementById("view_nombre_completo").textContent =
        data.nombre_completo;
      document.getElementById("view_dni").textContent = data.dni;
      document.getElementById("view_correo").textContent = data.correo;
      document.getElementById("view_fecha_registro").textContent =
        data.fecha_registro;
      document.getElementById("view_sexo").textContent = data.sexo;
      document.getElementById("view_ciudad").textContent =
        data.ciudad || "No especificada";

      // Foto de perfil
      const fotoElement = document.getElementById("view_foto");
      if (data.foto_perfil) {
        fotoElement.src = data.foto_perfil;
      } else {
        // Usar imagen por defecto
        fotoElement.src = "/static/img/profile_pics/foto_por_defecto.webp";
      }

      // Reportes
      const reportesList = document.getElementById("reportes_list");
      reportesList.innerHTML = "";

      if (data.reportes && data.reportes.length > 0) {
        data.reportes.forEach((reporte) => {
          const reporteItem = document.createElement("a");
          reporteItem.href = `/core/reportes/${reporte.id}/`;
          reporteItem.className = "reporte-item";
          reporteItem.textContent = `Reporte de Detección-R${String(
            reporte.id
          ).padStart(3, "0")}`;
          reportesList.appendChild(reporteItem);
        });
      } else {
        reportesList.innerHTML =
          '<p style="color: #999;">No hay reportes registrados</p>';
      }

      // Mostrar modal
      modal.style.display = "block";
    })
    .catch((error) => {
      showNotification("Error al cargar los detalles del paciente", "error");
    });
}

// ============================================
// ABRIR MODAL - CREAR NUEVO
// ============================================
function openModalCreate() {
  // Configurar título y modo
  modalTitle.textContent = "Registrar datos del paciente";
  viewMode.style.display = "none";
  formMode.style.display = "block";

  // Limpiar formulario
  patientForm.reset();
  document.getElementById("patient_id").value = "";
  document.getElementById("btnSubmit").textContent = "Registrar";

  // Limpiar errores
  clearErrors();

  // Reset preview de foto
  document.getElementById("preview_foto").src =
    "/static/img/profile_pics/foto_por_defecto.webp";

  // Mostrar modal
  modal.style.display = "block";
}

// ============================================
// ABRIR MODAL - EDITAR
// ============================================
function openModalEdit(patientId) {
  fetch(`/pacientes/${patientId}/`)
    .then((response) => response.json())
    .then((data) => {
      // Configurar título y modo
      modalTitle.textContent = "Editar datos del paciente";
      viewMode.style.display = "none";
      formMode.style.display = "block";

      // Llenar formulario
      document.getElementById("patient_id").value = data.id;
      document.getElementById("nombre").value = data.nombre;
      document.getElementById("apellido").value = data.apellido;
      document.getElementById("dni").value = data.dni;
      document.getElementById("correo").value = data.correo;
      document.getElementById("sexo").value =
        data.sexo === "Masculino" ? "M" : "F";
      document.getElementById("ciudad").value = data.ciudad || "";
      document.getElementById("direccion").value = data.direccion || "";

      // Foto de perfil
      const previewElement = document.getElementById("preview_foto");
      if (data.foto_perfil) {
        previewElement.src = data.foto_perfil;
      } else {
        previewElement.src = "/static/img/profile_pics/foto_por_defecto.webp";
      }

      document.getElementById("btnSubmit").textContent = "Actualizar";

      // Limpiar errores
      clearErrors();

      // Mostrar modal
      modal.style.display = "block";
    })
    .catch((error) => {
      showNotification("Error al cargar los datos del paciente", "error");
    });
}

// ============================================
// CERRAR MODAL
// ============================================
function closeModal() {
  modal.style.display = "none";
  patientForm.reset();
  clearErrors();
}

// Cerrar modal al hacer clic fuera de él
window.onclick = function (event) {
  if (event.target == modal) {
    closeModal();
  }
};

// ============================================
// PREVISUALIZAR IMAGEN
// ============================================
function previewImage(input) {
  if (input.files && input.files[0]) {
    const reader = new FileReader();

    reader.onload = function (e) {
      document.getElementById("preview_foto").src = e.target.result;
    };

    reader.readAsDataURL(input.files[0]);
  }
}

// ============================================
// LIMPIAR ERRORES
// ============================================
function clearErrors() {
  const errorMessages = document.querySelectorAll(".error-message");
  errorMessages.forEach((error) => {
    error.classList.remove("show");
    error.textContent = "";
  });

  const errorInputs = document.querySelectorAll(".form-control.error");
  errorInputs.forEach((input) => {
    input.classList.remove("error");
  });
}

// ============================================
// MOSTRAR ERRORES
// ============================================
function showErrors(errors) {
  clearErrors();

  for (const [field, message] of Object.entries(errors)) {
    const errorElement = document.getElementById(`error_${field}`);
    const inputElement = document.getElementById(field);

    if (errorElement && inputElement) {
      errorElement.textContent = message;
      errorElement.classList.add("show");
      inputElement.classList.add("error");
    }
  }
}

// ============================================
// ENVIAR FORMULARIO
// ============================================
patientForm.addEventListener("submit", function (e) {
  e.preventDefault();

  const patientId = document.getElementById("patient_id").value;
  const isEdit = patientId !== "";

  const formData = new FormData(patientForm);

  // Si no hay archivo seleccionado, eliminarlo del FormData
  if (!document.getElementById("foto_perfil").files[0]) {
    formData.delete("foto_perfil");
  }

  const url = isEdit ? `/pacientes/${patientId}/editar/` : "/pacientes/crear/";

  const btnSubmit = document.getElementById("btnSubmit");
  const originalText = btnSubmit.textContent;
  btnSubmit.disabled = true;
  btnSubmit.textContent = "Guardando...";

  fetch(url, {
    method: "POST",
    headers: {
      "X-CSRFToken": csrftoken,
    },
    body: formData,
  })
    .then((response) => {
      if (!response.ok) {
        return response.json().then((data) => {
          throw data;
        });
      }
      return response.json();
    })
    .then((data) => {
      if (data.success) {
        // Cerrar modal
        closeModal();

        // Verificar si estamos en la página de análisis
        const isAnalysisPage = window.location.pathname.includes("/analisis/");

        if (isAnalysisPage && !isEdit) {
          // Si es creación en página de análisis, disparar evento personalizado
          const event = new CustomEvent("pacienteCreated", {
            detail: data.paciente,
          });
          document.dispatchEvent(event);
          if (typeof showNotification === "function") {
            showNotification(
              `Paciente ${data.paciente.nombre} ${data.paciente.apellido} registrado correctamente`,
              "success"
            );
          }
        } else {
          // En otros casos, recargar la página - el mensaje se mostrará desde Django
          window.location.reload();
        }
      }
    })
    .catch((error) => {
      // Re-habilitar el botón en caso de error
      btnSubmit.disabled = false;
      btnSubmit.textContent = originalText;

      if (error.errors) {
        showErrors(error.errors);
        showNotification(
          "Por favor, corrige los errores en el formulario",
          "warning"
        );
      } else {
        showNotification(
          "Error al guardar el paciente. Por favor, intente nuevamente.",
          "error"
        );
      }
    });
});

// ============================================
// DRAG AND DROP PARA FOTO
// ============================================
const photoPreview = document.querySelector(".photo-preview");
const photoOverlay = document.querySelector(".photo-overlay");
const fotoInput = document.getElementById("foto_perfil");

if (photoPreview && fotoInput) {
  // Prevenir comportamiento por defecto
  photoPreview.addEventListener("dragover", (e) => {
    e.preventDefault();
    e.stopPropagation();
    photoPreview.style.borderColor = "#7fa8b5";
    photoPreview.style.borderWidth = "4px";
    photoPreview.style.borderStyle = "dashed";
    photoPreview.style.transform = "scale(1.05)";
    if (photoOverlay) {
      photoOverlay.style.background =
        "linear-gradient(to top, rgba(127, 168, 181, 0.95) 0%, rgba(127, 168, 181, 0.85) 70%, transparent 100%)";
    }
  });

  photoPreview.addEventListener("dragenter", (e) => {
    e.preventDefault();
    e.stopPropagation();
  });

  photoPreview.addEventListener("dragleave", (e) => {
    e.preventDefault();
    e.stopPropagation();
    // Solo resetear si realmente salimos del elemento
    if (e.target === photoPreview) {
      photoPreview.style.borderColor = "#e0e0e0";
      photoPreview.style.borderWidth = "3px";
      photoPreview.style.borderStyle = "solid";
      photoPreview.style.transform = "";
      if (photoOverlay) {
        photoOverlay.style.background =
          "linear-gradient(to top, rgba(95, 130, 145, 0.95) 0%, rgba(95, 130, 145, 0.85) 70%, transparent 100%)";
      }
    }
  });

  photoPreview.addEventListener("drop", (e) => {
    e.preventDefault();
    e.stopPropagation();

    // Restaurar estilos
    photoPreview.style.borderColor = "#e0e0e0";
    photoPreview.style.borderWidth = "3px";
    photoPreview.style.borderStyle = "solid";
    photoPreview.style.transform = "";
    if (photoOverlay) {
      photoOverlay.style.background =
        "linear-gradient(to top, rgba(95, 130, 145, 0.95) 0%, rgba(95, 130, 145, 0.85) 70%, transparent 100%)";
    }

    const files = e.dataTransfer.files;
    if (files.length > 0 && files[0].type.startsWith("image/")) {
      fotoInput.files = files;
      previewImage(fotoInput);
    } else {
      showNotification("Por favor, arrastra solo archivos de imagen", "error");
    }
  });

  // El click ya está manejado en el HTML con onclick
}
