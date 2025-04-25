document.addEventListener('DOMContentLoaded', function() {
  // ==================== CONFIGURACIÓN ====================
  const features = [
      {
          name: 'CalidadGeneral',
          label: 'Calidad General',
          value: null,
          format: (value) => ({
              '1': 'Muy Pobre', '2': 'Pobre', '3': 'Pobre', '4': 'Regular',
              '5': 'Regular', '6': 'Buena', '7': 'Buena', '8': 'Muy Buena',
              '9': 'Muy Buena', '10': 'Excelente'
          }[value] || value)
      },
      {
          name: 'MetrosHabitables',
          label: 'Metros Habitables',
          value: null,
          format: (value) => `${value} m²`
      },
      {
          name: 'CochesGaraje',
          label: 'Capacidad de Garaje',
          value: null,
          format: (value) => `${value} coche(s)`
      },
      {
          name: 'AñoConstrucción',
          label: 'Año de Construcción',
          value: null
      },
      {
          name: 'BañosCompletos',
          label: 'Baños Completos',
          value: null
      },
      {
          name: 'TotalHabitacionesSobreSuelo',
          label: 'Habitaciones',
          value: null
      },
      {
          name: 'Vecindario',
          label: 'Vecindario',
          value: null,
          format: (value) => ({
              'CollgCr': 'College Creek',
              'Veenker': 'Veenker',
              'Crawfor': 'Crawford',
              'NoRidge': 'Northridge',
              'Mitchel': 'Mitchell',
              'StoneBr': 'Stone Brook',
              'NWAmes': 'Northwest Ames',
              'OldTown': 'Old Town'
          }[value] || value)
      }
  ];

  const formWizard = document.getElementById('housing-wizard-form');
  if (!formWizard) return;

  // ==================== ESTADO ====================
  const totalSteps = 25;
  let currentStep = 1;
  let formSubmitted = sessionStorage.getItem('formSubmitted') === 'true';

  // ==================== ELEMENTOS UI ====================
  const elements = {
      prevBtn: document.getElementById('prev-btn'),
      nextBtn: document.getElementById('next-btn'),
      submitBtn: document.getElementById('submit-btn'),
      progressBar: document.getElementById('progress-bar'),
      stepCounter: document.getElementById('step-counter'),
      resetBtn: document.getElementById('reset-form'),
      descriptionContent: document.getElementById('description-content'),
      resultContent: document.getElementById('result-content'),
      priceDisplay: document.getElementById('price-display'),
      keyFeatures: document.getElementById('key-features'),
      loadingIndicator: document.createElement('div')
  };

  // Configuración inicial de UI
  elements.loadingIndicator.className = 'loader';
  elements.loadingIndicator.textContent = 'Calculando...';
  elements.prevBtn.style.display = 'none';
  elements.submitBtn.style.display = 'none';
  elements.descriptionContent.style.display = formSubmitted ? 'none' : 'block';
  elements.resultContent.style.display = formSubmitted ? 'block' : 'none';

  // ==================== FUNCIONES CORE ====================
  function updateFeatureValues() {
      features.forEach(feature => {
          const input = document.querySelector(`[name="${feature.name}"]`);
          if (input) {
              feature.value = input.type === 'radio' 
                  ? document.querySelector(`input[name="${feature.name}"]:checked`)?.value 
                  : input.value;
          }
      });
      
      sessionStorage.setItem('featuresData', JSON.stringify(
          features.filter(f => f.value !== null && f.value !== '')
      ));
      
      updateTemporaryFeaturesDisplay();
  }

  function updateTemporaryFeaturesDisplay() {
      if (!elements.priceDisplay || formSubmitted) return;
      
      const featuresWithValues = features.filter(f => f.value !== null && f.value !== '');
      
      elements.priceDisplay.innerHTML = featuresWithValues.length > 0
          ? `<div class="temp-features">${
              featuresWithValues.map(f => 
                  `<div><strong>${f.label}:</strong> ${
                      f.format ? f.format(f.value) : f.value
                  }</div>`
              ).join('')
            }</div>`
          : 'Complete el formulario para ver la estimación';
  }

  function updateKeyFeatures() {
      if (!elements.keyFeatures) return;
  
      const savedData = sessionStorage.getItem('featuresData');
      const featuresToShow = savedData ? JSON.parse(savedData) : 
          features.filter(f => f.value !== null && f.value !== '');
  
      elements.keyFeatures.innerHTML = featuresToShow.length === 0
          ? '<li>No hay datos suficientes</li>'
          : featuresToShow.map(f => {
              // Buscar la definición de la feature para obtener el formateador
              const featureDef = features.find(def => def.name === f.name);
              const formattedValue = featureDef?.format ? featureDef.format(f.value) : f.value;
              
              return `<li><strong>${featureDef?.label || f.label}:</strong> ${formattedValue}</li>`;
          }).join('');
  }

  function navigate(direction) {
      const newStep = currentStep + direction;
      if (newStep < 1 || newStep > totalSteps) return;
      
      if (direction > 0 && !validateCurrentStep()) return;
      
      currentStep = newStep;
      updateStep();
      window.scrollTo({top: formWizard.offsetTop - 20, behavior: 'smooth'});
  }

  function updateStep() {
      if (formSubmitted) return;
      
      document.querySelectorAll('.step-container').forEach(step => {
          step.classList.remove('active');
      });
      
      const currentStepEl = document.getElementById(`step-${currentStep}`);
      if (currentStepEl) currentStepEl.classList.add('active');
      
      // Actualizar UI
      elements.stepCounter.textContent = `Paso ${currentStep} de ${totalSteps}`;
      elements.progressBar.style.width = `${(currentStep / totalSteps) * 100}%`;
      
      elements.prevBtn.style.display = currentStep === 1 ? 'none' : 'block';
      elements.nextBtn.style.display = currentStep === totalSteps ? 'none' : 'block';
      elements.submitBtn.style.display = currentStep === totalSteps ? 'block' : 'none';
      
      applyFieldDependencies();
      clearErrorMessages();
      updateFeatureValues();
  }

  // ==================== ENVÍO Y RESULTADOS ====================
  async function submitToBackend() {
      try {
          // Mostrar estado de carga
          if (elements.priceDisplay) {
              elements.priceDisplay.innerHTML = '';
              elements.priceDisplay.appendChild(elements.loadingIndicator);
          }

          // Enviar el formulario de manera tradicional
          formWizard.submit();
          
          // Actualizar estado
          formSubmitted = true;
          sessionStorage.setItem('formSubmitted', 'true');
          
          // Actualizar UI
          if (elements.descriptionContent) {
              elements.descriptionContent.style.display = 'none';
          }
          if (elements.resultContent) {
              elements.resultContent.style.display = 'block';
          }
          
          // Actualizar características
          updateFeatureValues();
          updateKeyFeatures();

      } catch (error) {
          console.error('Error al enviar el formulario:', error);
          if (elements.priceDisplay) {
              elements.priceDisplay.innerHTML = 
                  '<div class="error">Error al calcular. Intente nuevamente.</div>';
              setTimeout(() => updateTemporaryFeaturesDisplay(), 3000);
          }
      }
  }

  function showPredictionResult(price) {
      formSubmitted = true;
      sessionStorage.setItem('formSubmitted', 'true');
      
      if (elements.priceDisplay) {
          elements.priceDisplay.innerHTML = `
              <div class="prediction-result">
                  <h3>Valor estimado:</h3>
                  <div class="price">$${Number(price).toLocaleString()}</div>
              </div>
          `;
      }
      
      if (elements.descriptionContent) {
          elements.descriptionContent.style.display = 'none';
      }
      if (elements.resultContent) {
          elements.resultContent.style.display = 'block';
      }
      updateKeyFeatures();
  }

  // ==================== VALIDACIÓN ====================
  function validateCurrentStep(isSubmission = false) {
      const currentStepEl = document.getElementById(`step-${currentStep}`);
      const inputs = currentStepEl.querySelectorAll('input[required], select[required]');
      let isValid = true;
  
      clearErrorMessages();
  
      inputs.forEach(input => {
          const isEmpty = (input.type === 'radio' && !document.querySelector(`input[name="${input.name}"]:checked`)) || 
                          (input.type !== 'radio' && !input.value.trim());
          
          if (isEmpty) {
              isValid = false;
              const errorMsg = document.createElement('div');
              errorMsg.className = 'error-message';
              errorMsg.textContent = 'Este campo es obligatorio';
              
              if (input.type !== 'radio') {
                  input.classList.add('error');
                  input.parentElement.appendChild(errorMsg);
              } else if (!input.closest('.option-buttons').querySelector('.error-message')) {
                  input.closest('.option-buttons').appendChild(errorMsg);
              }
          }
  
          // Validación específica para años
          if (input.type === 'number' && input.value && ['AñoConstrucción', 'AñoRenovación'].includes(input.id)) {
              const year = parseInt(input.value);
              if (year < 1800 || year > 2025) {
                  isValid = false;
                  input.classList.add('error');
                  const errorMsg = document.createElement('div');
                  errorMsg.className = 'error-message';
                  errorMsg.textContent = 'El año debe estar entre 1800 y 2025';
                  input.parentElement.appendChild(errorMsg);
              }
          }
  
          // Validación específica para números negativos
          if (input.type === 'number' && input.value && [
              'MetrosHabitables', 'ÁreaGaraje', 'MetrosTotalesSótano',
              'Metros1raPlanta', 'ÁreaRevestimientoMampostería',
              'MetrosAcabadosSótano1', 'FrenteLote'
          ].includes(input.id)) {
              const value = parseFloat(input.value);
              if (value < 0) {
                  isValid = false;
                  input.classList.add('error');
                  const errorMsg = document.createElement('div');
                  errorMsg.className = 'error-message';
                  errorMsg.textContent = 'El valor no puede ser negativo';
                  input.parentElement.appendChild(errorMsg);
              }
          }
      });
  
      return isValid;
  }
  
  function validateSingleField(field) {
      const container = field.closest('.form-group') || 
                       field.closest('.radio-group') || 
                       field.closest('.option-buttons');
      if (!container) return true;
  
      // Limpiar errores previos
      container.querySelectorAll('.error-message').forEach(el => el.remove());
      container.classList.remove('error');
      field.classList.remove('error');
  
      // Validar campo requerido
      if (field.hasAttribute('required')) {
          let isEmpty = false;
          
          if (field.type === 'radio') {
              const groupName = field.name;
              isEmpty = !document.querySelector(`input[name="${groupName}"]:checked`);
          } else {
              isEmpty = !field.value.trim();
          }
  
          if (isEmpty) {
              container.classList.add('error');
              field.classList.add('error');
              const errorMsg = document.createElement('div');
              errorMsg.className = 'error-message';
              errorMsg.textContent = 'Este campo es obligatorio';
              container.appendChild(errorMsg);
              return false;
          }
      }
  
      // Validación específica para años
      if (field.type === 'number' && field.value && ['AñoConstrucción', 'AñoRenovación'].includes(field.id)) {
          const year = parseInt(field.value);
          if (year < 1800 || year > new Date().getFullYear()) {
              field.classList.add('error');
              const errorMsg = document.createElement('div');
              errorMsg.className = 'error-message';
              errorMsg.textContent = `El año debe estar entre 1800 y ${new Date().getFullYear()}`;
              container.appendChild(errorMsg);
              return false;
          }
      }
  
      // Validación para números negativos
      if (field.type === 'number' && field.value && [
          'MetrosHabitables', 'ÁreaGaraje', 'MetrosTotalesSótano',
          'Metros1raPlanta', 'ÁreaRevestimientoMampostería',
          'MetrosAcabadosSótano1', 'FrenteLote'
      ].includes(field.id)) {
          const value = parseFloat(field.value);
          if (value < 0) {
              field.classList.add('error');
              const errorMsg = document.createElement('div');
              errorMsg.className = 'error-message';
              errorMsg.textContent = 'El valor no puede ser negativo';
              container.appendChild(errorMsg);
              return false;
          }
      }
  
      return true;
  }

  function clearErrorMessages() {
      document.querySelectorAll('.error-message').forEach(el => el.remove());
      document.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
      document.querySelectorAll('.error-label').forEach(el => el.remove()); 
  }

  // ==================== DEPENDENCIAS ENTRE CAMPOS ====================
  function applyFieldDependencies() {
      // Dependencia: CochesGaraje -> ÁreaGaraje
      if (currentStep === 4) {
          const cochesGaraje = document.querySelector('input[name="CochesGaraje"]:checked')?.value;
          const areaGaraje = document.getElementById('ÁreaGaraje');
          if (areaGaraje) {
              if (cochesGaraje === '0') {
                  areaGaraje.value = '0';
                  areaGaraje.readOnly = true;
              } else {
                  areaGaraje.readOnly = false;
              }
          }
      }

      // Dependencia: Chimeneas -> CalidadChimenea
      if (currentStep === 20) {
          const chimeneas = document.querySelector('input[name="Chimeneas"]:checked')?.value;
          document.querySelectorAll('input[name="CalidadChimenea"]').forEach(input => {
              const container = input.closest('.radio-option');
              if (chimeneas === '0') {
                  if (input.value === 'NoTiene') input.checked = true;
                  input.disabled = input.value !== 'NoTiene';
                  container.style.opacity = input.disabled ? '0.5' : '1';
              } else {
                  input.disabled = false;
                  container.style.opacity = '1';
              }
          });
      }
  }

  // ==================== MANEJO DE INPUTS ====================
  function setupInputTouchedState() {
      document.querySelectorAll('input, select').forEach(input => {
          input.addEventListener('blur', function() {
              this.dataset.touched = 'true';
              validateSingleField(this);
          });

          if (input.type === 'radio' || input.tagName === 'SELECT') {
              input.addEventListener('change', function() {
                  if (input.type === 'radio') {
                      document.querySelectorAll(`input[name="${this.name}"]`).forEach(radio => {
                          radio.dataset.touched = 'true';
                      });
                  } else {
                      this.dataset.touched = 'true';
                  }
                  validateSingleField(this);
              });
          }

          if (['text', 'number', 'email'].includes(input.type)) {
              let typingTimer;
              input.addEventListener('input', function() {
                  clearTimeout(typingTimer);
                  typingTimer = setTimeout(() => {
                      if (this.dataset.touched) validateSingleField(this);
                  }, 500);
              });
          }
      });
  }

  // ==================== RESET ====================
 // ==================== RESET ====================
 function resetFormCompletely() {
  // Resetear estado del formulario
  formWizard.reset();
  currentStep = 1;
  formSubmitted = false;
  
  // Resetear estado de las features
  features.forEach(f => f.value = null);
  
  // Limpiar almacenamiento
  sessionStorage.removeItem('formSubmitted');
  sessionStorage.removeItem('featuresData');
  
  // Resetear UI principal
  elements.descriptionContent.style.display = 'block';
  elements.resultContent.style.display = 'none';
  elements.priceDisplay.textContent = 'Complete el formulario para ver la estimación';
  
  // Limpiar TODOS los errores y estados
  document.querySelectorAll('.error').forEach(el => el.classList.remove('error'));
  document.querySelectorAll('.error-message').forEach(el => el.remove());
  document.querySelectorAll('[data-touched]').forEach(el => delete el.dataset.touched);
  
  // Resetear controles específicos
  document.querySelectorAll('input[type="radio"]').forEach(radio => {
      radio.checked = false;
      radio.disabled = false;
      const container = radio.closest('.radio-group, .option-buttons');
      if (container) container.style.opacity = '1';
  });
  
  document.querySelectorAll('select').forEach(select => {
      select.selectedIndex = 0;
  });
  
  document.querySelectorAll('input[readonly]').forEach(input => {
      input.readOnly = false;
  });
  
  // Restablecer dependencias y UI
  applyFieldDependencies();
  updateStep();
  
  // Scroll al inicio
  window.scrollTo({top: 0, behavior: 'smooth'});
}

  // ==================== INICIALIZACIÓN ====================
  setupInputTouchedState();
  updateStep();

  // Cargar última predicción si existe
  if (formSubmitted) {
      updateKeyFeatures();
      const lastPrediction = sessionStorage.getItem('featuresData');
      if (lastPrediction) {
          const featuresData = JSON.parse(lastPrediction);
          const precio = featuresData.find(f => f.name === 'precioPredicho')?.value;
          if (precio) {
              elements.priceDisplay.innerHTML = `
                  <div class="prediction-result">
                      <h3>Valor estimado:</h3>
                      <div class="price">$${Number(precio).toLocaleString()}</div>
                  </div>
              `;
          }
      }
  }

  // ==================== EVENT LISTENERS ====================
  elements.prevBtn.addEventListener('click', () => navigate(-1));
  elements.nextBtn.addEventListener('click', () => navigate(1));
  elements.submitBtn.addEventListener('click', async (e) => {
      e.preventDefault();
      if (validateCurrentStep(true)) {
          await submitToBackend();
      }
  });

  formWizard.addEventListener('submit', (e) => {
      if (!validateCurrentStep(true)) {
          e.preventDefault();
      }
  });

  formWizard.addEventListener('keypress', (e) => {
      if (e.key === 'Enter') {
          e.preventDefault();
          if (formSubmitted) return;
          currentStep < totalSteps ? elements.nextBtn.click() : elements.submitBtn.click();
      }
  });

  // Manejador del botón de reset usando delegación de eventos
  document.addEventListener('click', (e) => {
      if (e.target && e.target.id === 'reset-form') {
          e.preventDefault();
          resetFormCompletely();
      }
  });

  // Cursor retro
  document.body.style.cursor = 'url("data:image/svg+xml,<svg xmlns=\'http://www.w3.org/2000/svg\' width=\'24\' height=\'24\' viewBox=\'0 0 24 24\'><path fill=\'%23ff7f50\' d=\'M7,2H17L12,22L7,2Z\'/></svg>"), auto';
});