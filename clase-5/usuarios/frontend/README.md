# Frontend de Gestión de Usuarios y Planos

Aplicación frontend desarrollada con Vue 3 y Vite que proporciona una interfaz moderna y responsive para gestionar usuarios y planos. Este proyecto forma parte de un sistema más grande que interactúa con un backend API desarrollado con Node.js.

## Tecnologías Utilizadas

- **Vue 3**: Framework progresivo para construir interfaces de usuario
- **Vite**: Herramienta de construcción rápida para desarrollo frontend
- **Vue Router 4**: Enrutador oficial para Vue.js
- **Pinia**: Biblioteca de gestión de estado para Vue 3
- **Ant Design Vue 4**: Sistema de diseño UI para Vue
- **Node.js**: Entorno requerido (v20.19.0 o v22.12.0+)

## Estructura del Proyecto

```
frontend/
├── public/               # Archivos públicos estáticos
│   └── favicon.ico       # Icono de la aplicación
├── src/                  # Código fuente principal
│   ├── assets/           # Recursos estáticos (CSS, imágenes)
│   │   ├── base.css      # Estilos base
│   │   ├── logo.svg      # Logo de la aplicación
│   │   └── main.css      # Estilos principales
│   ├── components/       # Componentes reutilizables
│   │   ├── Plane/        # Componentes para gestión de planos
│   │   └── Users/        # Componentes para gestión de usuarios
│   ├── composable/       # Lógica reutilizable (composables de Vue)
│   │   ├── login/        # Lógica de autenticación
│   │   ├── plane/        # Lógica de gestión de planos
│   │   └── users/        # Lógica de gestión de usuarios
│   ├── layouts/          # Plantillas de diseño
│   │   ├── AuthLayout.vue    # Layout para usuarios autenticados
│   │   └── GuestLayout.vue   # Layout para usuarios no autenticados
│   ├── router/           # Configuración de rutas
│   │   └── index.js      # Definición de rutas de la aplicación
│   ├── services/         # Servicios para comunicación con API
│   ├── stores/           # Almacenes Pinia para gestión de estado
│   ├── utils/            # Utilidades y helpers
│   ├── views/            # Páginas/Vistas de la aplicación
│   │   ├── HomeView.vue      # Página de inicio
│   │   ├── LoginView.vue     # Página de inicio de sesión
│   │   ├── UsersView.vue     # Página de gestión de usuarios
│   │   └── PlaneView.vue     # Página de gestión de planos
│   ├── App.vue           # Componente raíz
│   └── main.js           # Punto de entrada de la aplicación
├── index.html            # Plantilla HTML principal
├── jsconfig.json         # Configuración JavaScript
├── package.json          # Dependencias y scripts
├── pnpm-lock.yaml        # Lock file de PNPM
├── vite.config.js        # Configuración de Vite
└── README.md             # Este archivo
```

## Características Principales

- **Sistema de autenticación**: Login y manejo de sesiones con JWT
- **Gestión de usuarios**: CRUD completo de usuarios
- **Gestión de planos**: Administración de planos/aviones
- **Diseño responsive**: Adaptable a diferentes dispositivos
- **Protección de rutas**: Acceso controlado según estado de autenticación
- **Layouts dinámicos**: Diferentes layouts para usuarios autenticados y visitantes

## Requisitos previos

- **Node.js**: versión ^20.19.0 o >=22.12.0
- **PNPM**: Gestor de paquetes (recomendado para este proyecto)

## Instalación

1. Clone el repositorio
```sh
git clone <url-del-repositorio>
cd usuarios/frontend
```

2. Instale las dependencias
```sh
pnpm install
```

3. Configure las variables de entorno (si es necesario)
Cree un archivo `.env.local` en la raíz del proyecto con la siguiente estructura:
```
VITE_API_URL=http://localhost:3000/api
```

## Scripts Disponibles

### Desarrollo

Inicia el servidor de desarrollo con hot-reload:
```sh
pnpm dev
```
La aplicación estará disponible en: [http://localhost:5173](http://localhost:5173)

### Compilación para producción

```sh
pnpm build
```
Los archivos compilados se generarán en el directorio `dist/`.

### Vista previa de producción

```sh
pnpm preview
```
Inicia un servidor local para previsualizar la versión compilada.

## Guía de Desarrollo

### Flujo de trabajo recomendado

1. Crear/modificar componentes en `src/components/`
2. Implementar lógica compartida en `src/composable/`
3. Definir servicios para comunicación con API en `src/services/`
4. Configurar estados globales en `src/stores/`
5. Crear o actualizar vistas en `src/views/`
6. Configurar rutas en `src/router/index.js`

### Herramientas recomendadas

- [VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (deshabilitar Vetur)
- [Vue Devtools](https://chrome.google.com/webstore/detail/vuejs-devtools/nhdogjmejiglipccpnnnanhbledajbpd)

## Convenciones de código

- **Nombres de componentes**: PascalCase (ej. UserList.vue)
- **Nombres de archivos de utilidades**: camelCase
- **Constantes**: UPPER_SNAKE_CASE
- **CSS**: Clases en kebab-case

## Despliegue

Para desplegar la aplicación:

1. Compile para producción
```sh
pnpm build
```

2. Despliegue los archivos de la carpeta `dist/` en su servidor web o servicio de hosting.

3. Para entornos que usan Node.js, puede servir los archivos estáticos con:
```sh
node server.js
```
(Requiere implementar un server.js sencillo que sirva los archivos estáticos)

## Integración con Backend

Esta aplicación frontend está diseñada para trabajar con un backend REST API. Para configurar la conexión:

1. Asegúrese de que el backend esté ejecutándose
2. Configure la URL de la API en su archivo `.env.local`:
```
VITE_API_URL=http://localhost:3000/api
```

## Solución de problemas

### Errores de CORS

Si encuentra errores de CORS:
1. Verifique que el backend tenga habilitado CORS
2. Confirme que las URLs de backend y frontend coincidan con la configuración

### Errores de autenticación

1. Limpie el localStorage del navegador
2. Verifique que los tokens JWT sean válidos
3. Confirme que las rutas protegidas requieran autenticación

---

**Autor**: Henry Vega  
**Versión**: 1.0  
**Fecha**: 2025
