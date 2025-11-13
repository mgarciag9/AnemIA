/**
 * ============================================
 * ANÁLISIS DE IMÁGENES - DETECCIÓN DE ANEMIA
 * ============================================
 */

// Variables globales
let croppedImageData = null;
let selectedPatientId = null;

// Variables para el canvas de selección
let drawingCanvas = null;
let maskCanvas = null;
let drawingCtx = null;
let maskCtx = null;
let isDrawing = false;
let brushSize = 20;
let originalImage = null;

// Variable para almacenar referencia al select de pacientes
let pacienteSelect = null;

// Escuchar evento de paciente creado ANTES de que se cargue el DOM
// para asegurar que siempre esté disponible
document.addEventListener("pacienteCreated", function (e) {
  const nuevoPaciente = e.detail;

  // Verificar que jQuery esté disponible
  if (typeof $ === "undefined") {
    if (typeof showNotification === "function") {
      showNotification("❌ jQuery no está disponible", "error");
    }
    return;
  }

  // Usar setTimeout para asegurar que Select2 esté completamente listo
  setTimeout(function () {
    if (!pacienteSelect) {
      pacienteSelect = document.getElementById("pacienteSelect");
    }

    if (pacienteSelect) {
      const $select = $(pacienteSelect);

      // Agregar paciente al select

      // Crear nueva opción
      const newOption = new Option(
        `${nuevoPaciente.nombre} ${nuevoPaciente.apellido} - DNI: ${nuevoPaciente.dni}`,
        nuevoPaciente.id,
        true, // defaultSelected
        true // selected
      );

      // Agregar la opción al select
      $select.append(newOption);

      // Seleccionar la nueva opción usando Select2
      $select.val(nuevoPaciente.id).trigger("change");

      // Actualizar la variable global
      selectedPatientId = nuevoPaciente.id;

      // Actualizar el botón de análisis
      if (typeof updateAnalyzeButton === "function") {
        updateAnalyzeButton();
      }

      // Mostrar notificación de éxito
      if (typeof showNotification === "function") {
        showNotification(
          `✅ Paciente ${nuevoPaciente.nombre} ${nuevoPaciente.apellido} registrado y seleccionado exitosamente`,
          "success"
        );
      }
    } else if (typeof showNotification === "function") {
      showNotification("❌ No se encontró el elemento pacienteSelect", "error");
    }
  }, 100); // Esperar 100ms para que Select2 esté listo
});

// Inicializar cuando el DOM esté listo
document.addEventListener("DOMContentLoaded", function () {
  initializeAnalysis();
});

/**
 * Inicializar todos los componentes
 */
function initializeAnalysis() {
  // Elementos del DOM
  const imageInput = document.getElementById("imageInput");
  const uploadArea = document.getElementById("uploadArea");
  const uploadPlaceholder = document.getElementById("uploadPlaceholder");
  const cropContainer = document.getElementById("cropContainer");
  const cropImage = document.getElementById("cropImage");
  const croppedPreview = document.getElementById("croppedPreview");
  const croppedImage = document.getElementById("croppedImage");
  pacienteSelect = document.getElementById("pacienteSelect"); // Asignar a variable global
  const btnAnalyze = document.getElementById("btnAnalyze");
  const btnNuevoPaciente = document.getElementById("btnNuevoPaciente");

  // Inicializar Select2 para búsqueda en el selector de pacientes
  $(pacienteSelect).select2({
    placeholder: "Selecciona a un paciente",
    allowClear: true,
    language: {
      noResults: function () {
        return "No se encontraron pacientes";
      },
      searching: function () {
        return "Buscando...";
      },
    },
  });

  // Event Listeners para selector de paciente
  $(pacienteSelect).on("change", function () {
    selectedPatientId = this.value;
    updateAnalyzeButton();
  });

  // Event Listener para botón nuevo paciente
  btnNuevoPaciente.addEventListener("click", function () {
    // Usar la función openModalCreate del archivo patients.js
    if (typeof openModalCreate === "function") {
      openModalCreate();
    } else {
      if (typeof showNotification === "function") {
        showNotification(
          "La función para crear paciente no está disponible",
          "error"
        );
      }
    }
  });

  // Click en el área de carga
  uploadPlaceholder.addEventListener("click", function () {
    imageInput.click();
  });

  // Drag & Drop
  uploadArea.addEventListener("dragover", function (e) {
    e.preventDefault();
    uploadPlaceholder.classList.add("drag-over");
  });

  uploadArea.addEventListener("dragleave", function (e) {
    e.preventDefault();
    uploadPlaceholder.classList.remove("drag-over");
  });

  uploadArea.addEventListener("drop", function (e) {
    e.preventDefault();
    uploadPlaceholder.classList.remove("drag-over");

    const files = e.dataTransfer.files;
    if (files.length > 0) {
      handleImageFile(files[0]);
    }
  });

  // Selección de archivo
  imageInput.addEventListener("change", function (e) {
    if (e.target.files.length > 0) {
      handleImageFile(e.target.files[0]);
    }
  });

  // Controles de selección
  const brushSizeSlider = document.getElementById("brushSize");
  const brushSizeValue = document.getElementById("brushSizeValue");

  brushSizeSlider.addEventListener("input", function () {
    brushSize = parseInt(this.value);
    brushSizeValue.textContent = brushSize + "px";
  });

  document.getElementById("btnClearMask").addEventListener("click", () => {
    clearMask();
  });

  document
    .getElementById("btnCancelSelection")
    .addEventListener("click", () => {
      cancelSelection();
    });

  document.getElementById("btnApplySelection").addEventListener("click", () => {
    applySelection();
  });

  // Cambiar imagen
  document.getElementById("btnChangeImage").addEventListener("click", () => {
    changeImage();
  });

  // Botón de análisis
  btnAnalyze.addEventListener("click", function () {
    performAnalysis();
  });
}

/**
 * Manejar archivo de imagen seleccionado
 */
function handleImageFile(file) {
  // Validar tipo de archivo
  if (!file.type.match("image/(jpeg|jpg|png)")) {
    showNotification(
      "Por favor, selecciona una imagen en formato JPEG o PNG",
      "error"
    );
    return;
  }

  // Validar tamaño (max 10MB)
  if (file.size > 10 * 1024 * 1024) {
    showNotification("La imagen es muy grande. Tamaño máximo: 10MB", "error");
    return;
  }

  // Leer archivo
  const reader = new FileReader();
  reader.onload = function (e) {
    initializeSelectionCanvas(e.target.result);
  };
  reader.readAsDataURL(file);
}

/**
 * Inicializar canvas de selección libre
 */
function initializeSelectionCanvas(imageData) {
  const uploadPlaceholder = document.getElementById("uploadPlaceholder");
  const selectionContainer = document.getElementById("selectionContainer");

  // Ocultar placeholder, mostrar selection container
  uploadPlaceholder.style.display = "none";
  selectionContainer.style.display = "block";

  // Obtener canvas
  drawingCanvas = document.getElementById("drawingCanvas");
  maskCanvas = document.getElementById("maskCanvas");
  drawingCtx = drawingCanvas.getContext("2d");
  maskCtx = maskCanvas.getContext("2d");

  // Cargar imagen
  originalImage = new Image();
  originalImage.onload = function () {
    // Ajustar tamaño del canvas a la imagen
    const maxWidth = 800;
    const maxHeight = 600;
    let width = originalImage.width;
    let height = originalImage.height;

    // Redimensionar si es necesario
    if (width > maxWidth) {
      height = (height * maxWidth) / width;
      width = maxWidth;
    }
    if (height > maxHeight) {
      width = (width * maxHeight) / height;
      height = maxHeight;
    }

    drawingCanvas.width = width;
    drawingCanvas.height = height;
    maskCanvas.width = width;
    maskCanvas.height = height;

    // Posicionar mask canvas exactamente sobre drawing canvas
    maskCanvas.style.position = "absolute";
    maskCanvas.style.top = "0";
    maskCanvas.style.left = "50%";
    maskCanvas.style.transform = "translateX(-50%)";

    // Dibujar imagen original
    drawingCtx.drawImage(originalImage, 0, 0, width, height);

    // Configurar eventos de dibujo
    setupDrawingEvents();
  };
  originalImage.src = imageData;
}

/**
 * Configurar eventos de dibujo en el canvas
 */
function setupDrawingEvents() {
  // Mouse events
  maskCanvas.addEventListener("mousedown", startDrawing);
  maskCanvas.addEventListener("mousemove", draw);
  maskCanvas.addEventListener("mouseup", stopDrawing);
  maskCanvas.addEventListener("mouseout", stopDrawing);

  // Touch events para móviles
  maskCanvas.addEventListener("touchstart", handleTouchStart);
  maskCanvas.addEventListener("touchmove", handleTouchMove);
  maskCanvas.addEventListener("touchend", stopDrawing);
}

/**
 * Iniciar dibujo
 */
function startDrawing(e) {
  isDrawing = true;
  const rect = maskCanvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  maskCtx.beginPath();
  maskCtx.arc(x, y, brushSize / 2, 0, Math.PI * 2);
  maskCtx.fillStyle = "rgba(107, 158, 178, 0.5)"; // Color del sistema con transparencia
  maskCtx.fill();
}

/**
 * Dibujar en el canvas
 */
function draw(e) {
  if (!isDrawing) return;

  const rect = maskCanvas.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;

  maskCtx.lineTo(x, y);
  maskCtx.lineWidth = brushSize;
  maskCtx.strokeStyle = "rgba(107, 158, 178, 0.5)";
  maskCtx.lineCap = "round";
  maskCtx.lineJoin = "round";
  maskCtx.stroke();

  maskCtx.beginPath();
  maskCtx.arc(x, y, brushSize / 2, 0, Math.PI * 2);
  maskCtx.fill();
  maskCtx.beginPath();
  maskCtx.moveTo(x, y);
}

/**
 * Detener dibujo
 */
function stopDrawing() {
  isDrawing = false;
  maskCtx.beginPath();
}

/**
 * Manejar touch start
 */
function handleTouchStart(e) {
  e.preventDefault();
  const touch = e.touches[0];
  const mouseEvent = new MouseEvent("mousedown", {
    clientX: touch.clientX,
    clientY: touch.clientY,
  });
  maskCanvas.dispatchEvent(mouseEvent);
}

/**
 * Manejar touch move
 */
function handleTouchMove(e) {
  e.preventDefault();
  const touch = e.touches[0];
  const mouseEvent = new MouseEvent("mousemove", {
    clientX: touch.clientX,
    clientY: touch.clientY,
  });
  maskCanvas.dispatchEvent(mouseEvent);
}

/**
 * Limpiar máscara de selección
 */
function clearMask() {
  if (maskCtx) {
    maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height);
  }
}

/**
 * Cancelar selección
 */
function cancelSelection() {
  const uploadPlaceholder = document.getElementById("uploadPlaceholder");
  const selectionContainer = document.getElementById("selectionContainer");

  selectionContainer.style.display = "none";
  uploadPlaceholder.style.display = "flex";

  // Limpiar canvas
  if (drawingCtx)
    drawingCtx.clearRect(0, 0, drawingCanvas.width, drawingCanvas.height);
  if (maskCtx) maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height);

  // Limpiar input
  document.getElementById("imageInput").value = "";

  // Resetear variables
  originalImage = null;
  isDrawing = false;
}

/**
 * Aplicar selección
 */
function applySelection() {
  if (!originalImage || !maskCanvas || !drawingCanvas) {
    showNotification(
      "Por favor, carga una imagen antes de continuar",
      "warning"
    );
    return;
  }

  // Verificar si hay algo dibujado
  const maskImageData = maskCtx.getImageData(
    0,
    0,
    maskCanvas.width,
    maskCanvas.height
  );
  let hasSelection = false;
  for (let i = 3; i < maskImageData.data.length; i += 4) {
    if (maskImageData.data[i] > 0) {
      hasSelection = true;
      break;
    }
  }

  // Si no hay selección, usar la imagen completa
  if (!hasSelection) {
    croppedImageData = drawingCanvas.toDataURL("image/jpeg", 0.95);
    showFinalPreview();
    return;
  }

  // Crear canvas para la máscara binaria (blanco donde se pintó, negro donde no)
  const binaryMaskCanvas = document.createElement("canvas");
  binaryMaskCanvas.width = maskCanvas.width;
  binaryMaskCanvas.height = maskCanvas.height;
  const binaryMaskCtx = binaryMaskCanvas.getContext("2d");

  // Convertir la máscara semi-transparente a una máscara binaria opaca
  binaryMaskCtx.drawImage(maskCanvas, 0, 0);
  const binaryImageData = binaryMaskCtx.getImageData(
    0,
    0,
    binaryMaskCanvas.width,
    binaryMaskCanvas.height
  );

  // Hacer la máscara completamente opaca donde hay pincel
  for (let i = 0; i < binaryImageData.data.length; i += 4) {
    if (binaryImageData.data[i + 3] > 0) {
      // Si hay algo de alpha
      binaryImageData.data[i] = 255; // R = blanco
      binaryImageData.data[i + 1] = 255; // G = blanco
      binaryImageData.data[i + 2] = 255; // B = blanco
      binaryImageData.data[i + 3] = 255; // A = opaco
    }
  }
  binaryMaskCtx.putImageData(binaryImageData, 0, 0);

  // Crear canvas final con la imagen recortada
  const resultCanvas = document.createElement("canvas");
  resultCanvas.width = drawingCanvas.width;
  resultCanvas.height = drawingCanvas.height;
  const resultCtx = resultCanvas.getContext("2d");

  // Dibujar imagen original
  resultCtx.drawImage(drawingCanvas, 0, 0);

  // Usar la máscara binaria para recortar
  resultCtx.globalCompositeOperation = "destination-in";
  resultCtx.drawImage(binaryMaskCanvas, 0, 0);

  // Convertir a base64
  croppedImageData = resultCanvas.toDataURL("image/jpeg", 0.95);

  // Mostrar vista previa final
  showFinalPreview();
}

/**
 * Mostrar vista previa final de la imagen
 */
function showFinalPreview() {
  const selectionContainer = document.getElementById("selectionContainer");
  const croppedPreview = document.getElementById("croppedPreview");
  const croppedImage = document.getElementById("croppedImage");

  croppedImage.src = croppedImageData;
  selectionContainer.style.display = "none";
  croppedPreview.style.display = "flex";

  // Limpiar canvas
  if (drawingCtx)
    drawingCtx.clearRect(0, 0, drawingCanvas.width, drawingCanvas.height);
  if (maskCtx) maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height);

  // Actualizar botón de análisis
  updateAnalyzeButton();
}

/**
 * Crear canvas circular a partir de imagen recortada
 */
function createCircularCanvas(sourceCanvas) {
  const size = Math.min(sourceCanvas.width, sourceCanvas.height);
  const canvas = document.createElement("canvas");
  canvas.width = size;
  canvas.height = size;

  const ctx = canvas.getContext("2d");

  // Crear clip circular
  ctx.beginPath();
  ctx.arc(size / 2, size / 2, size / 2, 0, Math.PI * 2);
  ctx.closePath();
  ctx.clip();

  // Dibujar imagen
  ctx.drawImage(sourceCanvas, 0, 0, size, size);

  return canvas;
}

/**
 * Cambiar imagen
 */
function changeImage() {
  const croppedPreview = document.getElementById("croppedPreview");
  const uploadPlaceholder = document.getElementById("uploadPlaceholder");

  croppedPreview.style.display = "none";
  uploadPlaceholder.style.display = "flex";

  croppedImageData = null;
  document.getElementById("imageInput").value = "";

  updateAnalyzeButton();
}

/**
 * Actualizar estado del botón de análisis
 */
function updateAnalyzeButton() {
  const btnAnalyze = document.getElementById("btnAnalyze");
  const hasPatient = selectedPatientId && selectedPatientId !== "";
  const hasImage = croppedImageData !== null;

  btnAnalyze.disabled = !(hasPatient && hasImage);
}

/**
 * Realizar análisis
 */
async function performAnalysis() {
  if (!selectedPatientId || !croppedImageData) {
    showNotification("Selecciona un paciente y carga una imagen", "error");
    return;
  }

  const btnAnalyze = document.getElementById("btnAnalyze");
  const btnText = btnAnalyze.querySelector(".btn-text");
  const btnLoader = btnAnalyze.querySelector(".btn-loader");

  // Mostrar loader
  btnAnalyze.disabled = true;
  btnText.style.display = "none";
  btnLoader.style.display = "inline-flex";

  try {
    // Preparar datos
    const formData = new FormData();
    formData.append("paciente_id", selectedPatientId);
    formData.append("image_data", croppedImageData);

    // Obtener token CSRF
    const csrfToken = document.querySelector(
      "[name=csrfmiddlewaretoken]"
    ).value;

    // Enviar solicitud
    const response = await fetch("/analysis/analyze/", {
      method: "POST",
      headers: {
        "X-CSRFToken": csrfToken,
      },
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Error ${response.status}: ${response.statusText}`);
    }

    const data = await response.json();

    if (data.success) {
      // Ocultar el loader del botón
      btnText.style.display = "inline";
      btnLoader.style.display = "none";
      btnAnalyze.disabled = false;

      // Guardar mensaje para mostrar en la página de resultados
      sessionStorage.setItem("analysisCompletedMessage", "true");

      // Mostrar modal de transición
      showTransitionModal();

      // Animar progreso de generación de diagnóstico
      animateTransitionProgress();

      // Redirigir a la página de resultados después de la animación
      setTimeout(() => {
        window.location.href = data.redirect_url;
      }, 3000);
    } else {
      showNotification(data.error || "Error al analizar la imagen", "error");
    }
  } catch (error) {
    showNotification("❌ Error de conexión: " + error.message, "error");
  } finally {
    // Ocultar loader del botón solo si hubo error (si no hay modal activo)
    if (
      !document.getElementById("transitionModal")?.classList.contains("active")
    ) {
      btnText.style.display = "inline";
      btnLoader.style.display = "none";
      btnAnalyze.disabled = false;
    }
  }
}

/**
 * Resetear análisis
 */
function resetAnalysis() {
  // Limpiar selector de paciente
  document.getElementById("pacienteSelect").value = "";
  selectedPatientId = null;

  // Limpiar imagen
  croppedImageData = null;
  document.getElementById("imageInput").value = "";

  // Resetear vistas
  document.getElementById("uploadPlaceholder").style.display = "flex";
  document.getElementById("selectionContainer").style.display = "none";
  document.getElementById("croppedPreview").style.display = "none";

  // Limpiar canvas si existen
  if (drawingCtx)
    drawingCtx.clearRect(0, 0, drawingCanvas.width, drawingCanvas.height);
  if (maskCtx) maskCtx.clearRect(0, 0, maskCanvas.width, maskCanvas.height);

  // Resetear variables
  originalImage = null;
  isDrawing = false;

  // Actualizar botón
  updateAnalyzeButton();
}

/**
 * Mostrar notificación
 */
// Las notificaciones se gestionan globalmente desde main.js

// Escuchar evento de paciente creado desde el modal
document.addEventListener("pacienteCreated", function (e) {
  const pacienteData = e.detail;

  // Agregar el nuevo paciente al selector
  const pacienteSelect = document.getElementById("pacienteSelect");
  const newOption = document.createElement("option");
  newOption.value = pacienteData.id;
  newOption.textContent = `${pacienteData.nombre} ${pacienteData.apellido} - DNI: ${pacienteData.dni}`;
  pacienteSelect.appendChild(newOption);

  // Seleccionar automáticamente el nuevo paciente
  pacienteSelect.value = pacienteData.id;
  selectedPatientId = pacienteData.id;

  // Actualizar el botón de análisis
  updateAnalyzeButton();

  // Mostrar mensaje de éxito
  if (typeof showNotification === "function") {
    showNotification(
      `Paciente ${pacienteData.nombre} ${pacienteData.apellido} registrado correctamente`,
      "success"
    );
  }
});
