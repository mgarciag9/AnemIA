// JavaScript principal del sistema

document.addEventListener("DOMContentLoaded", function () {
  // Funcionalidad del menú móvil (si es necesario en el futuro)
  const toggleSidebar = () => {
    const sidebar = document.querySelector(".sidebar");
    if (sidebar) {
      sidebar.classList.toggle("active");
    }
  };

  // Auto-ocultar mensajes después de 12 segundos
  const alerts = document.querySelectorAll(".alert");
  if (alerts.length > 0) {
    alerts.forEach((alert, index) => {
      // Agregar un pequeño retraso progresivo si hay múltiples alertas
      setTimeout(() => {
        if (alert.parentElement) {
          alert.style.transition = "all 0.5s ease";
          alert.style.transform = "translateX(120%)";
          alert.style.opacity = "0";
          setTimeout(() => {
            if (alert.parentElement) {
              alert.remove();
            }
          }, 500);
        }
      }, 12000 + index * 200);
    });
  }
});

// Notificaciones globales del proyecto
// Tipos: success, error, warning, info
window.showNotification = function (message, type = "info") {
  const alertTypes = {
    success: "alert-success",
    error: "alert-danger",
    warning: "alert-warning",
    info: "alert-info",
  };

  const alertClass = alertTypes[type] || "alert-info";

  // Crear elemento de notificación
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert ${alertClass} alert-dismissible fade show`;
  alertDiv.role = "alert";
  alertDiv.style.display = "flex";
  alertDiv.innerHTML = `
    ${message}
    <button type="button" class="btn-close" onclick="this.parentElement.remove()">
      <span aria-hidden="true">&times;</span>
    </button>
  `;

  // Buscar o crear contenedor de mensajes
  let messagesContainer = document.querySelector(".messages-container");
  if (!messagesContainer) {
    messagesContainer = document.createElement("div");
    messagesContainer.className = "messages-container";
    // Insertar después del navbar si existe
    const mainWrapper = document.querySelector(".main-wrapper");
    if (mainWrapper) {
      const navbar =
        mainWrapper.querySelector(".navbar") || mainWrapper.firstChild;
      if (navbar && navbar.nextSibling) {
        mainWrapper.insertBefore(messagesContainer, navbar.nextSibling);
      } else {
        mainWrapper.insertBefore(messagesContainer, mainWrapper.firstChild);
      }
    } else {
      document.body.appendChild(messagesContainer);
    }
  }

  // Agregar notificación al principio del contenedor
  messagesContainer.insertBefore(alertDiv, messagesContainer.firstChild);

  // Forzar reflow para animación
  alertDiv.offsetHeight;

  // Auto-ocultar después de 12 segundos
  const autoHideTimer = setTimeout(() => {
    if (alertDiv.parentElement) {
      alertDiv.style.transition = "all 0.5s ease";
      alertDiv.style.transform = "translateX(120%)";
      alertDiv.style.opacity = "0";
      setTimeout(() => {
        if (alertDiv.parentElement) {
          alertDiv.remove();
        }
      }, 500);
    }
  }, 12000);

  // Limpiar el timer si se cierra manualmente
  const closeBtn = alertDiv.querySelector(".btn-close");
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      clearTimeout(autoHideTimer);
    });
  }
};
