/**
 * ============================================
 * RESULTADOS DE ANÁLISIS - GESTIÓN DE REPORTES
 * ============================================
 */

// Variables globales
let reporteGuardado = false;
let reporteId = null;
let csrfToken = "";

/**
 * Inicializar la página de resultados
 */
function initializeResults(csrf) {
  csrfToken = csrf;

  // Mostrar notificación de análisis completado si viene desde análisis
  if (sessionStorage.getItem("analysisCompletedMessage") === "true") {
    sessionStorage.removeItem("analysisCompletedMessage");
    if (typeof showNotification === "function") {
      showNotification("✅ Análisis completado exitosamente", "success");
    }
  }

  // Guardar reporte automáticamente al cargar la página
  guardarReporteAutomaticamente();
}

/**
 * Guardar reporte automáticamente al cargar resultados
 */
async function guardarReporteAutomaticamente() {
  if (reporteGuardado) {
    console.log("Reporte ya guardado con ID:", reporteId);
    return true;
  }

  try {
    const formData = new FormData();
    formData.append(
      "paciente_id",
      document.getElementById("paciente_id").value
    );
    formData.append(
      "image_filename",
      document.getElementById("image_filename").value
    );
    formData.append(
      "observaciones",
      document.getElementById("observaciones").value
    );
    formData.append(
      "interpretacion",
      document.getElementById("interpretacion").value
    );
    formData.append(
      "recomendaciones",
      document.getElementById("recomendaciones").value
    );
    formData.append(
      "tiene_anemia",
      document.getElementById("tiene_anemia").value
    );
    formData.append(
      "probabilidad",
      document.getElementById("probabilidad").value
    );
    formData.append("confianza", document.getElementById("confianza").value);
    formData.append(
      "nivel_confianza",
      document.getElementById("nivel_confianza").value
    );

    const response = await fetch("/analysis/save/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      reporteGuardado = true;
      reporteId = data.reporte_id;

      if (data.created) {
        console.log("✅ Reporte guardado automáticamente con ID:", reporteId);
      } else {
        console.log("ℹ️ Reporte ya existía, actualizado con ID:", reporteId);
      }

      return true;
    } else {
      throw new Error(data.error || "Error al guardar reporte");
    }
  } catch (error) {
    console.error("Error al guardar reporte:", error);
    if (typeof showNotification === "function") {
      showNotification(
        "❌ Error al guardar reporte: " + error.message,
        "error"
      );
    }
    return false;
  }
}

/**
 * Generar PDF del reporte
 */
async function generarPDFReporte() {
  // Asegurarse de que el reporte esté guardado
  if (!reporteGuardado) {
    const guardado = await guardarReporteAutomaticamente();
    if (!guardado) {
      if (typeof showNotification === "function") {
        showNotification(
          "❌ Error: El reporte debe estar guardado para generar PDF",
          "error"
        );
      }
      return;
    }
  }

  if (!reporteId) {
    if (typeof showNotification === "function") {
      showNotification(
        "❌ Error: No se pudo obtener el ID del reporte",
        "error"
      );
    }
    return;
  }

  // Redirigir a la URL de generación de PDF
  if (typeof showNotification === "function") {
    showNotification("📄 Generando PDF del reporte...", "info");
  }

  // Abrir el PDF en una nueva pestaña o descargar directamente
  window.location.href = `/reportes/${reporteId}/generar-pdf/`;
}

/**
 * Mostrar modal de confirmación para cancelar
 */
function mostrarModalCancelar() {
  document.getElementById("confirmCancelModal").style.display = "block";
}

/**
 * Cerrar modal de confirmación
 */
function closeConfirmCancelModal() {
  document.getElementById("confirmCancelModal").style.display = "none";
}

/**
 * Confirmar cancelación - Elimina reporte e imagen
 */
async function confirmarCancelacionAnalisis() {
  try {
    // SIEMPRE eliminar el reporte de la base de datos si existe
    if (reporteGuardado && reporteId) {
      const deleteReportFormData = new FormData();
      deleteReportFormData.append("reporte_id", reporteId);

      const reportResponse = await fetch("/analysis/delete-report/", {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
        },
        body: deleteReportFormData,
      });

      const reportData = await reportResponse.json();

      if (reportData.success) {
        console.log("✅ Reporte eliminado de la base de datos");
      } else {
        console.warn("⚠️ No se pudo eliminar el reporte:", reportData.error);
      }
    }

    // Eliminar la imagen del servidor
    const formData = new FormData();
    formData.append(
      "paciente_id",
      document.getElementById("paciente_id").value
    );
    formData.append(
      "image_filename",
      document.getElementById("image_filename").value
    );

    const response = await fetch("/analysis/delete-image/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    });

    const data = await response.json();

    if (data.success) {
      console.log("✅ Imagen eliminada del servidor");

      if (typeof showNotification === "function") {
        showNotification("🗑️ Análisis cancelado y eliminado", "info");
      }

      // Redirigir al formulario de análisis
      setTimeout(() => {
        window.location.href = "/analysis/";
      }, 500);
    } else {
      throw new Error(data.error || "Error al eliminar imagen");
    }
  } catch (error) {
    console.error("Error al cancelar análisis:", error);
    if (typeof showNotification === "function") {
      showNotification("❌ Error: " + error.message, "error");
    }
  }
}

/**
 * Cerrar modal al hacer clic fuera de él
 */
window.addEventListener("click", function (event) {
  const modal = document.getElementById("confirmCancelModal");
  if (event.target === modal) {
    closeConfirmCancelModal();
  }
});
