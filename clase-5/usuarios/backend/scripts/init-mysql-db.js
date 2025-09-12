#!/usr/bin/env node

/**
 * Script para inicializar la base de datos MySQL con el esquema de empleados
 */

const mysql = require('mysql2/promise');
const fs = require('fs');
const path = require('path');
const dotenv = require('dotenv');

// Cargar variables de entorno
dotenv.config();

async function initializeDatabase() {
  console.log('🔄 Inicializando base de datos MySQL para empleados...');

  const {
    MYSQL_HOST = 'localhost',
    MYSQL_USER = 'root',
    MYSQL_PASSWORD = '',
    MYSQL_DATABASE = 'empleados_db',
    MYSQL_PORT = 3306
  } = process.env;

  try {
    // Primero conectarse sin especificar base de datos (para poder crearla)
    const connection = await mysql.createConnection({
      host: MYSQL_HOST,
      user: MYSQL_USER,
      password: MYSQL_PASSWORD,
      port: Number(MYSQL_PORT)
    });

    console.log('✅ Conexión a MySQL establecida');

    // Crear base de datos si no existe
    await connection.query(`CREATE DATABASE IF NOT EXISTS ${MYSQL_DATABASE} 
                          CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci`);
    console.log(`✅ Base de datos "${MYSQL_DATABASE}" creada o verificada`);

    // Cerrar la conexión inicial
    await connection.end();

    // Conectar a la base de datos específica
    const dbConnection = await mysql.createConnection({
      host: MYSQL_HOST,
      user: MYSQL_USER,
      password: MYSQL_PASSWORD,
      database: MYSQL_DATABASE,
      port: Number(MYSQL_PORT),
      multipleStatements: true // Permitir múltiples consultas en un solo query
    });

    // Leer el archivo SQL
    const sqlFilePath = path.join(__dirname, '..', 'src', 'database', 'empleados.sql');
    const sqlContent = fs.readFileSync(sqlFilePath, 'utf8');

    // Ejecutar el script SQL
    console.log('🔄 Ejecutando script SQL para crear tablas y datos iniciales...');
    await dbConnection.query(sqlContent);
    console.log('✅ Script SQL ejecutado correctamente');

    // Cerrar la conexión
    await dbConnection.end();

    console.log('✅ Base de datos MySQL inicializada exitosamente');
  } catch (error) {
    console.error('❌ Error al inicializar la base de datos:', error.message);
    process.exit(1);
  }
}

initializeDatabase();
