import { DataSource, DataSourceOptions } from 'typeorm';
import { EmpleadoEntity } from '../models/mysql/empleado.entity';
import { UserEntity } from '../models/mysql/user.entity';
import { configDotenv } from 'dotenv';

configDotenv();

// Configuración para TypeORM
const typeormConfig: DataSourceOptions = {
  type: 'mysql',
  host: process.env.MYSQL_HOST || '',
  port: parseInt(process.env.MYSQL_PORT || ''),
  username: process.env.MYSQL_USER || '',
  password: process.env.MYSQL_PASSWORD || '',
  database: process.env.MYSQL_DATABASE || '',
  entities: [EmpleadoEntity, UserEntity],
  synchronize: true, // En producción, cambia esto a false y usa migraciones
  logging: ['error', 'warn'],
  connectTimeout: 60000,
  extra: {
    connectionLimit: 10
  }
};

// Crear la instancia de DataSource
export const AppDataSource = new DataSource(typeormConfig);

// Variable para controlar si la conexión ya fue inicializada
let isInitialized = false;

// Función para inicializar la conexión de TypeORM
export const initializeTypeORM = async (): Promise<DataSource | null> => {
  if (isInitialized) {
    console.info('La conexión de TypeORM ya está inicializada');
    return AppDataSource;
  }

  try {
    console.info('Intentando conectar a MySQL con TypeORM...');
    if (!AppDataSource.isInitialized) {
      await AppDataSource.initialize();
    }
    isInitialized = true;
    console.info('Conexión de TypeORM establecida exitosamente');
    return AppDataSource;
  } catch (error: any) {
    console.error('Error al conectar con TypeORM:', error.message);
    return null;
  }
};

// Función para asegurarse de que la conexión esté inicializada antes de usarla
export const getDataSource = async (): Promise<DataSource> => {
  if (!AppDataSource.isInitialized) {
    await initializeTypeORM();
  }
  return AppDataSource;
};

// Exponer la configuración por si es necesaria en otro lugar
export { typeormConfig };
