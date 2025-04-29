// index.js - Script para formatear valores en la tabla de predicciones

document.addEventListener('DOMContentLoaded', function() {
  // Formatear la tabla de predicciones
  formatTableValues();
});

/**
* Formatea los valores en la tabla de predicciones para que coincidan con predict.html
*/
function formatTableValues() {
  // Formatear Calidad General
  document.querySelectorAll('.calidad-general').forEach(cell => {
      const value = parseInt(cell.textContent.trim());
      if (!isNaN(value)) {
          if (value === 1) cell.textContent = 'Muy Pobre';
          else if (value === 2 || value === 3) cell.textContent = 'Pobre';
          else if (value === 4 || value === 5) cell.textContent = 'Regular';
          else if (value === 6 || value === 7) cell.textContent = 'Buena';
          else if (value === 8 || value === 9) cell.textContent = 'Muy Buena';
          else if (value === 10) cell.textContent = 'Excelente';
      }
  });
  
  // Formatear Metros Habitables (añadir unidades)
  document.querySelectorAll('.metros-habitables').forEach(cell => {
      const value = cell.textContent.trim();
      if (value && !value.endsWith('m²')) {
          cell.textContent = value + ' m²';
      }
  });
  
  // Formatear Coches Garaje (añadir descriptor)
  document.querySelectorAll('.coches-garaje').forEach(cell => {
      const value = cell.textContent.trim();
      if (value && !value.includes('coche')) {
          cell.textContent = value + ' coche(s)';
      }
  });
  
  // Formatear Calidad Cocina
  document.querySelectorAll('.calidad-cocina').forEach(cell => {
      const value = cell.textContent.trim();
      if (value === 'Gd') cell.textContent = 'Buena';
      else if (value === 'TA') cell.textContent = 'Estándar';
      else if (value === 'Ex') cell.textContent = 'Excelente';
      else if (value === 'Fa') cell.textContent = 'Regular';
      else if (value === 'Po') cell.textContent = 'Pobre';
  });
}