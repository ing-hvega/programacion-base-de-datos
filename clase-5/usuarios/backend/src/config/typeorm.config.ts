import { createConnection, Connection, ConnectionOptions } from 'typeorm';
import { EmpleadoEntity } from '../models/empleado.entity';
import dotenv from 'dotenv';

dotenv.config();

// Configuración para TypeORM
const typeormConfig: ConnectionOptions = {
  type: 'mysql',
  host: process.env.MYSQL_HOST || 'localhost',
  port: parseInt(process.env.MYSQL_PORT || '3308'),
  username: process.env.MYSQL_USER || 'root',
  password: process.env.MYSQL_PASSWORD || 'root',
  database: process.env.MYSQL_DATABASE || 'empleados_db',
  entities: [EmpleadoEntity],
  synchronize: false, // En producción, cambia esto a false y usa migraciones
  logging: ['error', 'warn']
};

// Variable para almacenar la conexión
let connection: Connection;

// Función para inicializar la conexión de TypeORM
export const initializeTypeORM = async (): Promise<Connection | null> => {
  try {
    console.info('Intentando conectar a MySQL con TypeORM...');
    connection = await createConnection(typeormConfig);
    console.info('Conexión de TypeORM establecida exitosamente');
    return connection;
  } catch (error: any) {
    console.error('Error al conectar con TypeORM:', error.message);
    return null;
  }
};

// Función para obtener la conexión actual
export const getConnection = (): Connection => {
  if (!connection) {
    throw new Error('La conexión de TypeORM no ha sido inicializada');
  }
  return connection;
};

// Exponer la configuración por si es necesaria en otro lugar
export { typeormConfig };
