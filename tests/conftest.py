import os
import sys
import pytest
from unittest.mock import patch, MagicMock

# Añadir la ruta del proyecto al path para poder importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def app():
    """Fixture que proporciona una instancia de la aplicación Flask para pruebas."""
    from app import create_app
    
    # Usar configuración de desarrollo que apunta al modelo real
    app = create_app('development')
    app.config.update({
        'TESTING': True,
        # Usar el modelo real de la aplicación
        'MODEL_PATH': 'model/modelo_ridge_california_housing.pkl'
    })
    
    # Contexto de aplicación
    with app.app_context():
        yield app

@pytest.fixture
def client(app):
    """Fixture que proporciona un cliente de prueba para hacer solicitudes HTTP."""
    return app.test_client()

@pytest.fixture
def mock_db():
    """Fixture que proporciona un mock de la conexión a la base de datos."""
    with patch('app.utils.db_utils.mysql') as mock:
        connection_mock = MagicMock()
        cursor_mock = MagicMock()
        
        # Configurar el mock para devolver un ID al insertar
        cursor_mock.lastrowid = 123
        connection_mock.cursor.return_value = cursor_mock
        mock.connection = connection_mock
        
        yield mock

@pytest.fixture
def sample_form_data():
    """Fixture que proporciona datos de ejemplo para el formulario."""
    return {
        'CalidadGeneral': '7',
        'MetrosHabitables': '150.5',
        'CochesGaraje': '2',
        'ÁreaGaraje': '45.0',
        'MetrosTotalesSótano': '80.0',
        'Metros1raPlanta': '90.0',
        'BañosCompletos': '2',
        'TotalHabitacionesSobreSuelo': '5',
        'AñoConstrucción': '2000',
        'AñoRenovación': '2010',
        'ÁreaRevestimientoMampostería': '30.0',
        'Chimeneas': '1',
        'MetrosAcabadosSótano1': '40.0',
        'FrenteLote': '20.0',
        'CalidadExterior': 'Gd',
        'CalidadCocina': 'Gd',
        'CalidadSótano': 'TA',
        'AcabadoGaraje': 'Fin',
        'AireAcondicionadoCentral': 'Y',
        'CalidadChimenea': 'TA',
        'Cimentación': 'PConc',
        'TipoGaraje': 'Attchd',
        'TipoRevestimientoMampostería': 'BrkFace',
        'CalidadCalefacción': 'Ex',
        'Vecindario': 'CollgCr'
    }