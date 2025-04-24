-- Datos iniciales para la base de datos (opcional)
USE housing_predictions;

-- Usuario administrador (contraseña: admin123)
INSERT INTO users (username, password_hash, email) 
VALUES ('admin', '$2b$12$tG/xZ.bLzK0SFB.YlJx1peSgEvE7xTCwB7XrGQJ.iVNUfEHvQiEPG', 'admin@example.com');