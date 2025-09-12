import mysql from 'mysql2/promise';

// Pool de conexiones para MySQL
export const pool = mysql.createPool({
    host: process.env.MYSQL_HOST || 'localhost',
    user: process.env.MYSQL_USER || 'root',
    password: process.env.MYSQL_PASSWORD || 'root',
    database: process.env.MYSQL_DATABASE || 'empleados_db',
    port: parseInt(process.env.MYSQL_PORT || '3308')
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
