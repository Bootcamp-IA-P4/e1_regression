/**
 * California Dreamin' - Formulario de Pasarela para Predicción de Valor de Vivienda
 * Estilo retro años 90
 */
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
            if (errorElement) {
                errorElement.remove();
            }
            
            // Eliminar clase de error
            if (input.classList) {
                input.classList.remove('error');
            }
            
            // Validar campos requeridos
            if ((input.type === 'radio' && !getSelectedValueById(input.name)) || 
                (input.type !== 'radio' && !input.value)) {
                
                isValid = false;
                
                // Para radios, marcar error solo una vez por grupo
                if (input.type !== 'radio' || !input.parentElement.parentElement.querySelector('.error-message')) {
                    // Añadir mensaje de error
                    const errorMsg = document.createElement('div');
                    errorMsg.className = 'error-message';
                    errorMsg.textContent = 'Este campo es obligatorio';
                    
                    // Para inputs normales, añadir después del input
                    if (input.type !== 'radio') {
                        input.classList.add('error');
                        input.parentElement.appendChild(errorMsg);
                    } 
                    // Para radios, añadir después del contenedor de opciones
                    else {
                        input.parentElement.parentElement.appendChild(errorMsg);
                    }
                }
            }
        });
        
        return isValid;
    }
    
    /**
     * Maneja el envío del formulario para mostrar resultados
     */
    function handleSubmitForm(e) {
        // Si no pasamos la validación, prevenir envío
        if (!validateCurrentStep()) {
            e.preventDefault();
            return;
        }
        
        // En entorno de demostración, prevenimos el envío real y mostramos una simulación
        // En producción, este bloque se puede comentar para permitir el envío real al servidor
        e.preventDefault();
        
        // Ocultar el formulario
        formWizard.style.display = 'none';
        
        // Mostrar el panel de resultados
        document.getElementById('description-content').style.display = 'none';
        const resultContent = document.getElementById('result-content');
        resultContent.style.display = 'block';
        
        // Generar un precio simulado
        const predictedValue = Math.floor(Math.random() * 500000) + 200000;
        document.getElementById('predicted-value').textContent = '$' + predictedValue.toLocaleString();
        
        // Mostrar características clave
        showKeyFeatures();
    }
    
    /**
     * Muestra las características clave de la vivienda
     */
    function showKeyFeatures() {
        const keyFeatures = document.getElementById('key-features');
        keyFeatures.innerHTML = ''; // Limpiar lista
        
        // Características importantes a mostrar
        const features = [
            { name: 'CalidadGeneral', label: 'Calidad General' },
            { name: 'MetrosHabitables', label: 'Área Habitable', unit: 'm²' },
            { name: 'TotalHabitacionesSobreSuelo', label: 'Habitaciones' },
            { name: 'BañosCompletos', label: 'Baños' },
            { name: 'AñoConstrucción', label: 'Año de Construcción' },
            { name: 'Vecindario', label: 'Vecindario' }
        ];
        
        // Obtener valores y agregar a la lista
        features.forEach(feature => {
            let value;
            try {
                value = feature.name === 'Vecindario' 
                    ? document.querySelector(`input[name="${feature.name}"]:checked + label`).textContent
                    : getSelectedValueById(feature.name) || document.getElementById(feature.name).value;
            } catch (e) {
                value = "No especificado";
            }
                
            if (value) {
                const li = document.createElement('li');
                li.innerHTML = `<strong>${feature.label}:</strong> ${value}${feature.unit || ''}`;
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