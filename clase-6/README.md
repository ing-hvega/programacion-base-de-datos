# Guía de Instalación y Configuración: Plataforma Multi-Servicio con Docker

Esta guía detalla el proceso para instalar y configurar la AMI específica **amazon/al2023-ami-2023.8.20250908.0-kernel-6.1-x86_64** en AWS EC2 y posteriormente configurar nuestro entorno multi-servicio con Docker, que incluye Nginx, Apache, Node.js y Traefik como proxy inverso con soporte HTTPS.

## Índice
1. [Requisitos Previos](#requisitos-previos)
2. [Lanzar una Instancia EC2 con Amazon Linux 2023](#lanzar-una-instancia-ec2-con-amazon-linux-2023)
3. [Configuración Inicial del Servidor](#configuración-inicial-del-servidor)
4. [Instalación de Docker y Docker Compose](#instalación-de-docker-y-docker-compose)
5. [Arquitectura del Sistema](#arquitectura-del-sistema)
6. [Despliegue de la Aplicación](#despliegue-de-la-aplicación)
7. [Configuración de DuckDNS](#configuración-de-duckdns)
8. [Solución de Problemas Comunes](#solución-de-problemas-comunes)
9. [Instalación Automatizada con Script](#instalación-automatizada-con-script)
10. [Mantenimiento](#mantenimiento)

## Requisitos Previos

* Cuenta de AWS activa
* Conocimientos básicos de EC2 y AWS Management Console
* Cliente SSH para conectarse a la instancia
* Par de claves de EC2 creado o existente
* Dominios configurados en DuckDNS para los diferentes servicios:
  - demo-idat.duckdns.org (Nginx)
  - apache-ida.duckdns.org (Apache)
  - backend-idat.duckdns.org (Node.js)
  - traefik.demo-idat.duckdns.org (Panel de Traefik)
* Token de DuckDNS activo: 869ef39d-7141-4d47-9e8e-8ede1b6ab9e6

## Lanzar una Instancia EC2 con Amazon Linux 2023

1. **Inicia sesión** en la [AWS Management Console](https://aws.amazon.com/console/)

2. **Navega al servicio EC2** y haz clic en "Launch Instance"

3. **Nombra tu instancia** de manera descriptiva (ej. "demo-idat-server")

4. **Selecciona la AMI específica**:
   - Haz clic en "Browse more AMIs"
   - Selecciona "AWS Marketplace AMIs"
   - En la barra de búsqueda, introduce: `amazon/al2023-ami-2023.8.20250908.0-kernel-6.1-x86_64`
   - Selecciona la AMI que coincida exactamente con este ID

5. **Selecciona el tipo de instancia**:
   - Recomendado: t2.micro (capa gratuita) para pruebas o t2.small/t2.medium para producción
   - Asegúrate de que el tipo de instancia sea compatible con la arquitectura x86_64

6. **Configura los detalles de la instancia**:
   - Par de claves: Selecciona un par de claves existente o crea uno nuevo
   - Configuración de red: Selecciona una VPC y subred adecuadas
   - Grupo de seguridad: Crea uno nuevo con los siguientes puertos abiertos:
     * SSH (22) - Restringido a tu IP
     * HTTP (80) - Abierto a todo el tráfico (0.0.0.0/0)
     * HTTPS (443) - Abierto a todo el tráfico (0.0.0.0/0)

7. **Configura almacenamiento**:
   - Tamaño mínimo recomendado: 20 GB

8. **Revisa y lanza** la instancia
   - Haz clic en "Launch Instance"

9. **Espera** a que la instancia se inicialice (puede tomar unos minutos)

## Configuración Inicial del Servidor

1. **Conéctate a tu instancia** mediante SSH:
   ```bash
   ssh -i /ruta/a/tu/clave.pem ec2-user@tu-ip-publica
   ```

2. **Actualiza el sistema**:
   ```bash
   sudo dnf update -y
   ```

3. **Instala herramientas básicas**:
   ```bash
   sudo dnf install -y git vim wget curl htop
   ```

## Instalación de Docker y Docker Compose

1. **Instala Docker**:
   ```bash
   sudo dnf install -y docker
   sudo systemctl enable docker
   sudo systemctl start docker
   sudo usermod -aG docker ec2-user
   ```
   
   Para aplicar los cambios de grupo, cierra sesión y vuelve a iniciarla:
   ```bash
   exit
   # Vuelve a conectarte mediante SSH
   ```

2. **Instala Docker Compose**:
   ```bash
   sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```

3. **Verifica las instalaciones**:
   ```bash
   docker --version
   docker-compose --version
   ```

## Arquitectura del Sistema

Nuestro sistema está compuesto por varios servicios Docker coordinados a través de Docker Compose:

1. **Nginx (Puerto 81)**
   - Servicio web ligero para contenido estático
   - Configurado en el subdominio: demo-idat.duckdns.org

2. **Apache (Puerto 82)**
   - Servicio web alternativo con capacidades adicionales
   - Configurado en el subdominio: apache-ida.duckdns.org

3. **Backend Node.js (Puerto 3000)**
   - API REST basada en Express.js
   - Ofrece endpoints para la aplicación
   - Configurado en el subdominio: backend-idat.duckdns.org

4. **Traefik (Puertos 80/443)**
   - Actúa como proxy inverso y balanceador de carga
   - Gestiona certificados SSL automáticos vía Let's Encrypt
   - Panel de administración en: traefik.demo-idat.duckdns.org

5. **DuckDNS**
   - Actualiza automáticamente las direcciones IP en los registros DNS
   - Permite el acceso a los servicios a través de nombres de dominio fijos

Todos los servicios están interconectados a través de una red Docker interna llamada `traefik-network`.

## Despliegue de la Aplicación

1. **Clona el repositorio de la aplicación**:
   ```bash
   mkdir -p /home/ec2-user/app
   cd /home/ec2-user/app
   git clone https://tu-repositorio.git .
   ```

2. **Configura el archivo .env**:
   ```bash
   cd docker-deploy
   vim .env
   ```

   Asegúrate de que contenga la siguiente información (ajusta según tus necesidades):
   ```
   # Configuración DuckDNS
   DUCKDNS_TOKEN=869ef39d-7141-4d47-9e8e-8ede1b6ab9e6
   DUCKDNS_SUBDOMAIN=demo-idat,apache-ida,backend-idat
   DUCKDNS_TZ=America/Lima

   # Configuración Traefik
   TRAEFIK_ADMIN_USER=admin
   TRAEFIK_ADMIN_PASSWORD_HASH=$apr1$NX6OCEqn$wLhJ8Ht8/b.n92ZPKUpS31
   TRAEFIK_ACME_EMAIL=tu-email@gmail.com

   # Configuración de dominios
   NGINX_DOMAIN=demo-idat.duckdns.org
   APACHE_DOMAIN=apache-ida.duckdns.org
   BACKEND_DOMAIN=backend-idat.duckdns.org
   TRAEFIK_DASHBOARD_DOMAIN=traefik.demo-idat.duckdns.org
   
   # IP pública para Apache (si es necesario)
   APACHE_IP=38.25.51.39
   ```

3. **Compila la imagen del backend Node.js**:
   ```bash
   cd docker-deploy
   chmod +x build-backend-image.sh
   ./build-backend-image.sh
   ```

4. **Inicia todos los servicios**:
   ```bash
   docker-compose up -d
   ```

5. **Verifica que los contenedores estén funcionando**:
   ```bash
   docker-compose ps
   ```

6. **Verifica los logs de cada servicio**:
   ```bash
   docker-compose logs nginx
   docker-compose logs apache
   docker-compose logs backend
   docker-compose logs traefik
   ```

## Configuración de DuckDNS

1. **Asegúrate de que tu dominio en DuckDNS apunte a la IP pública de tu instancia EC2**:
   - Visita [DuckDNS](https://www.duckdns.org/) e inicia sesión
   - Actualiza tu subdominio `demo-idat` para que apunte a la IP pública de tu instancia EC2: `34.203.102.210`
   - El servicio duckdns incluido en el docker-compose mantendrá esta IP actualizada automáticamente

2. **Verifica la propagación DNS**:
   ```bash
   nslookup demo-idat.duckdns.org
   ```

## Solución de Problemas Comunes

### Los certificados SSL no se generan

1. **Verifica los logs de Traefik**:
   ```bash
   docker-compose logs traefik
   ```

2. **Asegúrate de que los puertos 80 y 443 estén abiertos** en el grupo de seguridad de AWS

3. **Verifica la conectividad a los dominios**:
   ```bash
   curl -I http://demo-idat.duckdns.org
   curl -I http://apache-ida.duckdns.org
   curl -I http://backend-idat.duckdns.org
   ```

4. **Comprueba que el correo electrónico sea válido**:
   - Let's Encrypt rechaza dominios como example.com
   - Usa un correo electrónico real en TRAEFIK_ACME_EMAIL

### Problemas con el servicio Node.js

1. **Verifica que la imagen se haya construido correctamente**:
   ```bash
   docker images | grep backend-idat
   ```

2. **Examina los logs del contenedor**:
   ```bash
   docker-compose logs backend
   ```

3. **Accede al contenedor para depuración**:
   ```bash
   docker-compose exec backend sh
   # Dentro del contenedor
   node -v
   ls -la
   cat server.js
   ```

4. **Prueba la API directamente**:
   ```bash
   curl http://localhost:3000/health
   ```

### El servicio de Nginx no se inicia

1. **Verifica los logs**:
   ```bash
   docker-compose logs nginx
   ```

2. **Asegúrate de que la configuración de Nginx sea correcta**:
   ```bash
   docker-compose exec nginx nginx -t
   ```

### Errores de permisos en Docker

1. **Asegúrate de que el usuario actual pertenezca al grupo docker**:
   ```bash
   groups
   ```

2. **Si es necesario, vuelve a agregar el usuario al grupo docker**:
   ```bash
   sudo usermod -aG docker $USER
   ```

## Mantenimiento

### Actualización de la aplicación

1. **Detén los servicios**:
   ```bash
   cd /home/ec2-user/app/docker-deploy
   docker-compose down
   ```

2. **Actualiza el código fuente**:
   ```bash
   cd /home/ec2-user/app
   git pull
   ```

3. **Reconstruye la imagen del backend si es necesario**:
   ```bash
   cd docker-deploy
   ./build-backend-image.sh
   ```

4. **Reinicia los servicios**:
   ```bash
   docker-compose up -d
   ```

### Backup de los certificados y datos

Los certificados Let's Encrypt se almacenan en la carpeta `letsencrypt`. Es recomendable hacer una copia de seguridad regularmente:

```bash
cd /home/ec2-user/app/docker-deploy
tar -czvf letsencrypt-backup-$(date +%Y%m%d).tar.gz letsencrypt/
```

### Rotación de logs

Para evitar que los logs ocupen demasiado espacio:

```bash
docker-compose logs --tail=1000 > recent_logs.txt
docker system prune -f  # Eliminar contenedores parados y recursos no utilizados
```

### Actualización de las imágenes base

Periódicamente, actualiza las imágenes base para obtener parches de seguridad:

```bash
docker-compose pull  # Actualiza las imágenes de los servicios
docker-compose up -d --build  # Reconstruye y reinicia los servicios
```

## Instalación Automatizada con Script

Para facilitar la instalación de Docker y Docker Compose, puedes utilizar el siguiente script de comandos que automatiza todo el proceso:

```bash
#!/bin/bash
# Script para instalar Docker y Docker Compose en Amazon Linux 2023

# Actualizar el sistema
echo "Actualizando el sistema..."
sudo dnf update -y

# Instalar dependencias
echo "Instalando dependencias..."
sudo dnf install -y git docker

# Habilitar y arrancar el servicio Docker
echo "Habilitando y arrancando Docker..."
sudo systemctl enable docker
sudo systemctl start docker

# Instalar Docker Compose
echo "Instalando Docker Compose..."
sudo curl -L "https://github.com/docker/compose/releases/download/v2.11.2/docker-compose-Linux-x86_64" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Crear grupo Docker si no existe
echo "Configurando grupos..."
sudo groupadd -f docker

# Añadir el usuario actual al grupo Docker
echo "Añadiendo el usuario al grupo docker..."
sudo usermod -aG docker $USER

# Reiniciar Docker
echo "Reiniciando Docker..."
sudo systemctl restart docker

echo "Instalación completada. Por favor, cierra la sesión y vuelve a iniciarla para que los cambios de grupo surtan efecto."
```

Guarda este script como `install-docker.sh` y ejecútalo con:

```bash
chmod +x install-docker.sh
./install-docker.sh
```

Después de ejecutar el script, cierra la sesión y vuelve a iniciarla para que los cambios de grupo surtan efecto. Luego verifica la instalación con:

```bash
docker --version
docker-compose --version
```

Este script es equivalente a las tareas de Ansible mencionadas en la documentación y proporciona una forma rápida de configurar el entorno necesario para nuestra aplicación.

## Recursos Adicionales

- [Documentación oficial de Docker](https://docs.docker.com/)
- [Documentación de Traefik](https://doc.traefik.io/traefik/)
- [Guía de DuckDNS](https://www.duckdns.org/spec.jsp)
- [Express.js (para el backend)](https://expressjs.com/es/)

---

Si tienes alguna pregunta o problema durante la instalación, por favor contáctanos a través de [soporte@ejemplo.com](mailto:soporte@ejemplo.com).

---

Última actualización: Septiembre 2025
