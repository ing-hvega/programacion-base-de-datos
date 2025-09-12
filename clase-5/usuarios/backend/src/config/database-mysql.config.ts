import mysql from 'mysql2/promise';
import {configDotenv} from "dotenv";

configDotenv()

// Pool de conexiones para MySQL
export const pool = mysql.createPool({
    host: process.env.MYSQL_HOST || '',
    user: process.env.MYSQL_USER || '',
    password: process.env.MYSQL_PASSWORD || '',
    database: process.env.MYSQL_DATABASE || '',
    port: parseInt(process.env.MYSQL_PORT || '')
});

// Función para conectar a MySQL
export const connectMySQLDB = async () => {
  try {
    console.info('Intentando conectar a MySQL...');
    const connection = await pool.getConnection();
    console.info("Conectado a MySQL exitosamente");
    connection.release();
    return true;
  } catch (e: any) {
    console.error("Error al conectar a MySQL:", e.message);
    return false;
  }
};

// Función para ejecutar consultas SQL
export const query = async (sql: string, params: any[] = []) => {
  try {
    const [results] = await pool.execute(sql, params);
    return results;
  } catch (error: any) {
    console.error('Error en la consulta SQL:', error.message);
    throw error;
  }
};
