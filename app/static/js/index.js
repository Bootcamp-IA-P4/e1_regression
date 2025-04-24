document.addEventListener('DOMContentLoaded', function() {
    // Verificar si estamos en la página del formulario
    const formWizard = document.getElementById('housing-wizard-form');
    if (!formWizard) return;
    
    // Configuración
    const totalSteps = 25; // Total de pasos en el formulario
    let currentStep = 1;
    
    // Elementos DOM
    const prevBtn = document.getElementById('prev-btn');
    const nextBtn = document.getElementById('next-btn');
    const submitBtn = document.getElementById('submit-btn');
    const progressBar = document.getElementById('progress-bar');
    const stepCounter = document.getElementById('step-counter');
    const resetBtn = document.getElementById('reset-form');
    
    // Inicializar estado de los botones
    prevBtn.style.display = 'none';
    submitBtn.style.display = 'none';
    
    /**
     * Actualiza la visualización para mostrar el paso actual
     */
    function updateStep() {
        // Ocultar todos los pasos con efecto fade-out
        document.querySelectorAll('.step-container').forEach(step => {
            step.classList.remove('active');
        });
        
        // Mostrar el paso actual con efecto fade-in
        const currentStepElement = document.getElementById(`step-${currentStep}`);
        if (currentStepElement) {
            currentStepElement.classList.add('active');
        }
        
        // Actualizar el contador de pasos
        stepCounter.textContent = `Paso ${currentStep} de ${totalSteps}`;
        
        // Actualizar la barra de progreso con animación suave
        const progressPercentage = (currentStep / totalSteps) * 100;
        progressBar.style.width = `${progressPercentage}%`;
        
        // Mostrar/ocultar botones según el paso actual
        if (currentStep === 1) {
            prevBtn.style.display = 'none';
        } else {
            prevBtn.style.display = 'block';
        }
        
        if (currentStep === totalSteps) {
            nextBtn.style.display = 'none';
            submitBtn.style.display = 'block';
        } else {
            nextBtn.style.display = 'block';
            submitBtn.style.display = 'none';
        }
        
        // Aplicar dependencias entre campos
        applyFieldDependencies();
    }
    
    /**
     * Aplica dependencias entre campos
     * Por ejemplo, si no hay garaje (0 coches), deshabilita campos relacionados
     */
    function applyFieldDependencies() {
        // Dependencia: CochesGaraje y ÁreaGaraje
        if (currentStep === 4) { 
            const cochesGaraje = getSelectedValueById('CochesGaraje');
            const areaGarajeInput = document.getElementById('ÁreaGaraje');
            
            if (cochesGaraje === '0') {
                areaGarajeInput.value = '0';
                areaGarajeInput.setAttribute('readonly', 'readonly');
            } else {
                areaGarajeInput.removeAttribute('readonly');
            }
        }
        
        // Dependencia: Chimeneas y CalidadChimenea
        if (currentStep === 20) {
            const chimeneas = getSelectedValueById('Chimeneas');
            const calidadChimeneaInputs = document.querySelectorAll('input[name="CalidadChimenea"]');
            
            if (chimeneas === '0') {
                // Seleccionar automáticamente "NoTiene"
                calidadChimeneaInputs.forEach(input => {
                    if (input.value === 'NoTiene') {
                        input.checked = true;
                    }
                    
                    // Deshabilitar todas excepto "NoTiene"
                    if (input.value !== 'NoTiene') {
                        input.disabled = true;
                        input.parentElement.style.opacity = '0.5';
                    }
                });
            } else {
                // Habilitar todas las opciones
                calidadChimeneaInputs.forEach(input => {
                    input.disabled = false;
                    input.parentElement.style.opacity = '1';
                });
            }
        }
        
        // Dependencia: Metros Sótano y Calidad Sótano
        if (currentStep === 17) {
            const metrosSotano = document.getElementById('MetrosTotalesSótano').value;
            const calidadSotanoInputs = document.querySelectorAll('input[name="CalidadSótano"]');
            
            if (metrosSotano === '0') {
                // Seleccionar automáticamente "NoSótano"
                calidadSotanoInputs.forEach(input => {
                    if (input.value === 'NoSótano') {
                        input.checked = true;
                    }
                    
                    // Deshabilitar todas excepto "NoSótano"
                    if (input.value !== 'NoSótano') {
                        input.disabled = true;
                        input.parentElement.style.opacity = '0.5';
                    }
                });
            } else {
                // Habilitar todas las opciones
                calidadSotanoInputs.forEach(input => {
                    input.disabled = false;
                    input.parentElement.style.opacity = '1';
                });
            }
        }
    }
    
    /**
     * Obtiene el valor seleccionado de inputs radio por su name
     */
    function getSelectedValueById(name) {
        const selectedInput = document.querySelector(`input[name="${name}"]:checked`);
        return selectedInput ? selectedInput.value : '';
    }
    
    /**
     * Valida que todos los campos requeridos en el paso actual estén completos
     */
    function validateCurrentStep() {
        const currentStepElement = document.getElementById(`step-${currentStep}`);
        const inputs = currentStepElement.querySelectorAll('input[required], select[required]');
        let isValid = true;
        inputs.forEach(input => {
            // Eliminar mensajes de error previos
            const errorElement = input.parentElement.querySelector('.error-message');
            if (errorElement) errorElement.remove();
            input.classList.remove('error');
            // Validar campos requeridos
            if ((input.type === 'radio' && !getSelectedValueById(input.name)) || 
                (input.type !== 'radio' && !input.value.trim())) {
                isValid = false;
                // Para radios, marcar error solo una vez por grupo
                if (input.type !== 'radio' || !input.parentElement.parentElement.querySelector('.error-message')) {
                    const errorMsg = document.createElement('div');
                    errorMsg.className = 'error-message';
                    errorMsg.textContent = 'Requerido';
                    if (input.type !== 'radio') {
                        input.classList.add('error');
                        input.parentElement.appendChild(errorMsg);
                    } else {
                        input.parentElement.parentElement.appendChild(errorMsg);
                    }
                }
            }
        });
        return isValid;
    }
    
    /**
     * Maneja el envío del formulario para la predicción del modelo ML
     */
    function handleSubmitForm(e) {
        e.preventDefault();
        
        // Mostrar los valores ingresados en consola
        const formData = new FormData(formWizard);
        const values = {};
        formData.forEach((value, key) => { values[key] = value; });
        console.log('Valores ingresados:', values);
        
        // Validar TODOS los pasos, no solo el actual
        let allValid = true;
        let firstInvalidStep = null;
        for (let step = 1; step <= totalSteps; step++) {
            const stepElement = document.getElementById(`step-${step}`);
            if (!stepElement) continue;
            const inputs = stepElement.querySelectorAll('input[required], select[required]');
            
            inputs.forEach(input => {
                // Eliminar mensajes de error previos
                const errorElement = input.parentElement.querySelector('.error-message');
                if (errorElement) errorElement.remove();
                if (input.classList) input.classList.remove('error');
                
                if ((input.type === 'radio' && !getSelectedValueById(input.name)) || 
                    (input.type !== 'radio' && !input.value.trim())) {
                    allValid = false;
                    if (!firstInvalidStep) firstInvalidStep = step;
                    input.classList.add('error');
                    if (!input.parentElement.querySelector('.error-message')) {
                        const errorMsg = document.createElement('div');
                        errorMsg.className = 'error-message';
                        errorMsg.textContent = 'Requerido';
                        input.parentElement.appendChild(errorMsg);
                    }
                }
            });
        }
        
        if (!allValid) {
            alert('Por favor complete todos los campos requeridos antes de enviar.');
            if (firstInvalidStep) {
                currentStep = firstInvalidStep;
                updateStep();
            }
            return;
        }
        
        // Mostrar carga
        const loadingIndicator = document.createElement('div');
        loadingIndicator.className = 'loading-indicator';
        loadingIndicator.innerHTML = '<p>Calculando predicción...</p>';
        document.querySelector('.form-panel').appendChild(loadingIndicator);
        
        // Enviar usando el método tradicional del formulario
        formWizard.submit();
    }
    
    /**
     * Función auxiliar para formatear valores monetarios
     */
    function formatCurrency(value) {
        return '$' + value.toLocaleString('en-US', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    }
    
    /**
     * Función para mostrar información adicional basada en el valor predicho
     */
    function displayAdditionalInfo(predictedValue) {
        const infoElement = document.getElementById('additional-info');
        let message = '';
        
        if (predictedValue > 500000) {
            message = '¡Propiedad de lujo! Esta vivienda está en el top 10% del mercado.';
        } else if (predictedValue > 300000) {
            message = 'Propiedad de gama alta. Excelente inversión para familias.';
        } else if (predictedValue > 150000) {
            message = 'Vivienda estándar. Buen equilibrio entre precio y comodidad.';
        } else {
            message = 'Oportunidad de inversión. Propiedad con buen potencial de revalorización.';
        }
        
        infoElement.textContent = message;
    }
    
    /**
     * Muestra las características utilizadas en la predicción
     */
    function displayFeatures(inputData) {
        const keyFeatures = document.getElementById('key-features');
        keyFeatures.innerHTML = ''; // Limpiar lista
        
        // Mapeo de nombres de características a etiquetas más legibles
        const featureLabels = {
            'CalidadGeneral': 'Calidad General',
            'MetrosHabitables': 'Área Habitable',
            'TotalHabitacionesSobreSuelo': 'Habitaciones',
            'BañosCompletos': 'Baños',
            'AñoConstrucción': 'Año de Construcción',
            'Vecindario': 'Vecindario',
            'CochesGaraje': 'Espacios de Garaje',
            'Chimeneas': 'Número de Chimeneas',
            'MetrosTotalesSótano': 'Área de Sótano'
        };
        
        // Unidades para ciertas características
        const featureUnits = {
            'MetrosHabitables': ' m²',
            'ÁreaGaraje': ' m²',
            'MetrosTotalesSótano': ' m²',
            'Metros1raPlanta': ' m²',
            'ÁreaRevestimientoMampostería': ' m²',
            'MetrosAcabadosSótano1': ' m²',
            'FrenteLote': ' m'
        };
        
        // Mostrar las características más importantes
        const importantFeatures = [
            'CalidadGeneral', 
            'MetrosHabitables', 
            'TotalHabitacionesSobreSuelo', 
            'BañosCompletos', 
            'AñoConstrucción', 
            'Vecindario',
            'CochesGaraje',
            'Chimeneas',
            'MetrosTotalesSótano'
        ];
        
        importantFeatures.forEach(feature => {
            if (inputData.hasOwnProperty(feature)) {
                const li = document.createElement('li');
                const displayValue = typeof inputData[feature] === 'number' && featureUnits[feature] 
                    ? inputData[feature] + featureUnits[feature] 
                    : inputData[feature];
                
                li.innerHTML = `<strong>${featureLabels[feature] || feature}:</strong> ${displayValue}`;
                keyFeatures.appendChild(li);
            }
        });
    }
    
    /**
     * Animación de transición entre pasos
     */
    function animateStepTransition(direction = 'next') {
        const currentStepElement = document.getElementById(`step-${currentStep}`);
        
        // Animar salida
        currentStepElement.style.transition = 'opacity 0.3s, transform 0.3s';
        currentStepElement.style.opacity = '0';
        currentStepElement.style.transform = direction === 'next' ? 'translateX(-20px)' : 'translateX(20px)';
        
        // Animar entrada después de un pequeño delay
        setTimeout(() => {
            currentStepElement.style.opacity = '1';
            currentStepElement.style.transform = 'translateX(0)';
        }, 50);
    }
    
    // Event Listener para botón Anterior
    prevBtn.addEventListener('click', function() {
        if (currentStep > 1) {
            currentStep--;
            updateStep();
            animateStepTransition('prev');
            window.scrollTo({top: formWizard.offsetTop - 20, behavior: 'smooth'});
        }
    });
    
    // Event Listener para botón Siguiente
    nextBtn.addEventListener('click', function() {
        if (validateCurrentStep()) {
            if (currentStep < totalSteps) {
                currentStep++;
                updateStep();
                animateStepTransition('next');
                window.scrollTo({top: formWizard.offsetTop - 20, behavior: 'smooth'});
            }
        }
    });

    // Habilitar avanzar con radio/select al cambiar
    document.querySelectorAll('input[required], select[required]').forEach(input => {
        input.addEventListener('change', function() {
            // Si el input pertenece al paso actual, revalida y actualiza el botón Siguiente
            const stepElement = document.getElementById(`step-${currentStep}`);
            if (stepElement && stepElement.contains(input)) {
                // Si el campo requerido ya está completo, intenta avanzar automáticamente
                if (validateCurrentStep()) {
                    nextBtn.disabled = false;
                } else {
                    nextBtn.disabled = true;
                }
            }
        });
    });
    
    // Event Listener para botón Enviar
    submitBtn.addEventListener('click', handleSubmitForm);
    
    // Event Listener para prevenir envío con Enter
    formWizard.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            if (currentStep < totalSteps) {
                nextBtn.click();
            } else {
                submitBtn.click();
            }
        }
    });
    
    // Event Listener para el formulario
    formWizard.addEventListener('submit', handleSubmitForm);
    
    // Event Listener para botón de reinicio
    if (resetBtn) {
        resetBtn.addEventListener('click', function() {
            // Reiniciar el formulario
            formWizard.reset();
            formWizard.style.display = 'block';
            
            // Ocultar resultado y mostrar descripción
            document.getElementById('description-content').style.display = 'block';
            document.getElementById('result-content').style.display = 'none';
            
            // Volver al paso 1
            currentStep = 1;
            updateStep();
        });
    }
    
    // Configurar dependencias entre campos
    document.querySelectorAll('input[name="CochesGaraje"]').forEach(input => {
        input.addEventListener('change', function() {
            if (currentStep === 4) {
                applyFieldDependencies();
            }
        });
    });
    
    document.querySelectorAll('input[name="Chimeneas"]').forEach(input => {
        input.addEventListener('change', function() {
            if (currentStep === 20) {
                applyFieldDependencies();
            }
        });
    });
    
    // Inicializar el formulario
    updateStep();
});