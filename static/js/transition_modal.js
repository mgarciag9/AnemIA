/**
 * ============================================
 * MODAL DE TRANSICIÓN - GESTIÓN DE CARGA
 * ============================================
 */

/**
 * Mostrar modal de transición a resultados
 */
function showTransitionModal() {
  const modal = document.getElementById("transitionModal");
  if (modal) {
    modal.classList.add("active");
    // Prevenir scroll del body cuando el modal está abierto
    document.body.style.overflow = "hidden";
  }
}

/**
 * Ocultar modal de transición
 */
function hideTransitionModal() {
  const modal = document.getElementById("transitionModal");
  if (modal) {
    modal.classList.remove("active");
    document.body.style.overflow = "";
  }
}

/**
 * Animar barra de progreso del modal
 */
function animateTransitionProgress() {
  const progressFill = document.getElementById("progressFill");
  const statusText = document.getElementById("transitionStatus");

  if (!progressFill || !statusText) return;

  const steps = [
    { progress: 30, text: "Analizando imagen...", delay: 0 },
    { progress: 60, text: "Generando diagnóstico con IA...", delay: 1000 },
    { progress: 90, text: "Preparando reporte...", delay: 2000 },
    { progress: 100, text: "Completado", delay: 2800 },
  ];

  steps.forEach((step) => {
    setTimeout(() => {
      progressFill.style.width = step.progress + "%";
      statusText.textContent = step.text;
    }, step.delay);
  });
}
