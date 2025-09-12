import { connectDB } from "./config/database-mongo.config";
import { configDotenv } from "dotenv";
import cors from 'cors';
import express from "express";
import userRouter from "./routes/mongodb/user.router";
import loginRouter from "./routes/mongodb/login.router";
import planeRouter from "./routes/mongodb/plane.router";

import empleadoRouterOrm from "./routes/mysql/empleado.router";
import userRouterOrm from "./routes/mysql/user.router.orm";
import authRouterOrm from "./routes/mysql/auth.router";

import { connectMySQLDB } from "./config/database-mysql.config";
import { initializeTypeORM } from "./config/typeorm.config";

// Configurar variables de entorno antes de cualquier otra operación
configDotenv();

const PORT = process.env.PORT || 3000;
const app = express();

// Configuración de middleware
app.use(cors());
app.use(express.json());

// Inicializar conexiones a bases de datos
const initializeApp = async () => {
  try {
    console.log('Iniciando la aplicación...');

    // Inicializar TypeORM para las entidades
    const typeormConnection = await initializeTypeORM();
    if (!typeormConnection) {
      throw new Error('No se pudo establecer la conexión con TypeORM');
    }

    // También mantenemos las otras conexiones si son necesarias
    // await connectDB(); // MongoDB
    const mysqlConnected = await connectMySQLDB(); // MySQL directo
    if (!mysqlConnected) {
      console.warn('Advertencia: No se pudo establecer la conexión directa a MySQL. Algunas funciones podrían no estar disponibles.');
    }

    // Ruta principal para verificar que el servidor está funcionando
    app.get('/', (req, res) => res.json({
      status: 'ok',
      message: 'API funcionando correctamente'
    }));

    // Rutas existentes
    app.use('/api', userRouter);
    app.use('/api', loginRouter);
    app.use('/api', planeRouter);

    // Nuevas rutas para usuarios y autenticación con MySQL
    app.use('/api', authRouterOrm);
    app.use('/api', empleadoRouterOrm);
    app.use('/api', userRouterOrm);

    // Middleware para rutas no encontradas
    app.use((req, res) => {
      res.status(404).json({
        success: false,
        message: 'Ruta no encontrada'
      });
    });

    // Iniciar el servidor
    app.listen(PORT, () => {
      console.log(`Servidor iniciado en el puerto ${PORT}`);
      console.log(`API disponible en http://localhost:${PORT}`);
    });
  } catch (error: any) {
    console.error('Error fatal al inicializar la aplicación:', error.message);
    process.exit(1);
  }
};

// Iniciar la aplicación
initializeApp().catch(error => {
  console.error('Error no controlado durante la inicialización:', error);
  process.exit(1);
});
