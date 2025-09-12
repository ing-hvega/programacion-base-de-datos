// Importación de dependencias
const express = require('express');
const cors = require('cors');
const morgan = require('morgan');
const dotenv = require('dotenv');

// Cargar variables de entorno
dotenv.config();

// Inicializar express
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(morgan('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Rutas básicas
app.get('/', (req, res) => {
  res.json({
    message: 'API de Backend IDAT funcionando correctamente',
    status: 'online',
    version: '1.0.0'
  });
});

// Ruta de estado de salud
app.get('/health', (req, res) => {
  res.status(200).json({
    status: 'UP',
    timestamp: new Date().toISOString(),
    uptime: process.uptime(),
    environment: process.env.NODE_ENV || 'development'
  });
});

// Ruta de ejemplo para obtener datos
app.get('/api/data', (req, res) => {
  const exampleData = [
    { id: 1, name: 'Proyecto 1', description: 'Descripción del proyecto 1' },
    { id: 2, name: 'Proyecto 2', description: 'Descripción del proyecto 2' },
    { id: 3, name: 'Proyecto 3', description: 'Descripción del proyecto 3' }
  ];

  res.json(exampleData);
});

// Middleware para manejo de errores 404
app.use((req, res, next) => {
  res.status(404).json({
    error: 'Not Found',
    message: `La ruta ${req.originalUrl} no existe en este servidor`
  });
});

// Middleware para manejo de errores
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).json({
    error: 'Internal Server Error',
    message: err.message || 'Ocurrió un error en el servidor'
  });
});

// Iniciar el servidor
app.listen(PORT, () => {
  console.log(`Servidor backend-idat ejecutándose en http://localhost:${PORT}`);
  console.log(`Ambiente: ${process.env.NODE_ENV || 'development'}`);
});
