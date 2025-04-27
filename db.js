require('dotenv').config();
const mysql = require('mysql2');

// Crear la conexión usando variables del .env
const connection = mysql.createConnection({
  host: process.env.MYSQL_HOST,
  user: process.env.MYSQL_USER,
  password: process.env.MYSQL_PASSWORD,
  database: process.env.MYSQL_DB
});

// Probar la conexión
connection.connect((err) => {
  if (err) {
    console.error('Error de conexión:', err.stack);
    return;
  }
  console.log('Conectado a MySQL como id ' + connection.threadId);
});

// Exportar la conexión para usar en otros archivos
module.exports = connection;
