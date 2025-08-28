# Sistema de Base de Datos de Ventas - Diccionario de Datos

## Resumen General
Sistema completo de base de datos de ventas con 20 tablas interconectadas diseñado para operaciones de ventas a nivel empresarial. Este sistema gestiona todo, desde datos geográficos básicos hasta transacciones de ventas complejas, gestión de inventario y operaciones financieras.

**Nombre de la Base de Datos:** `sales_system`  
**Conjunto de Caracteres:** `utf8mb4`  
**Colación:** `utf8mb4_unicode_ci`  
**Total de Tablas:** 20

---

## Estructura de Tablas y Relaciones

### 1. **countries** - Datos Maestros de Países
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del país |
| `name` | VARCHAR(100) | NOT NULL | Nombre del país |
| `iso_code` | VARCHAR(3) | NOT NULL, UNIQUE | Código de país ISO 3166-1 alfa-3 |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Propósito:** Tabla maestra para países utilizados en todo el sistema  
**Relaciones:** Referenciada por la tabla `regions`

---

### 2. **regions** - Estados/Provincias/Regiones
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único de la región |
| `name` | VARCHAR(100) | NOT NULL | Nombre de la región/estado |
| `country_id` | INT | NOT NULL, FK | Referencia a la tabla countries |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Propósito:** Subdivisión geográfica dentro de los países  
**Relaciones:** 
- Padre: `countries(id)`
- Hijo: tabla `cities`

---

### 3. **cities** - Datos Maestros de Ciudades
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único de la ciudad |
| `name` | VARCHAR(100) | NOT NULL | Nombre de la ciudad |
| `region_id` | INT | NOT NULL, FK | Referencia a la tabla regions |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Propósito:** Datos geográficos a nivel de ciudad para direcciones y ubicaciones  
**Relaciones:** 
- Padre: `regions(id)`
- Referenciada por: `employees`, `customers`, `suppliers`, `warehouses`

---

### 4. **users** - Usuarios del Sistema
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del usuario |
| `email` | VARCHAR(150) | NOT NULL, UNIQUE | Dirección de correo electrónico del usuario |
| `password_hash` | VARCHAR(255) | NOT NULL | Contraseña hasheada por seguridad |
| `first_name` | VARCHAR(100) | NOT NULL | Nombre del usuario |
| `last_name` | VARCHAR(100) | NOT NULL | Apellido del usuario |
| `phone` | VARCHAR(20) | NULL | Número de teléfono de contacto |
| `birth_date` | DATE | NULL | Fecha de nacimiento |
| `status` | ENUM | DEFAULT 'active' | Estado de la cuenta del usuario |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |
| `updated_at` | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Marca de tiempo de última actualización |

**Valores de Estado:**
- `active`: El usuario puede acceder al sistema
- `inactive`: Cuenta de usuario deshabilitada
- `suspended`: Suspensión temporal

**Propósito:** Datos base de autenticación de usuarios y perfil  
**Relaciones:** Referenciada por `employees` y `customers`

---

### 5. **employees** - Empleados de la Empresa
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del empleado |
| `user_id` | INT | NOT NULL, UNIQUE, FK | Referencia a la tabla users |
| `employee_code` | VARCHAR(20) | NOT NULL, UNIQUE | Código interno del empleado |
| `position` | VARCHAR(100) | NOT NULL | Título del trabajo/posición |
| `salary` | DECIMAL(10,2) | NULL | Salario mensual |
| `hire_date` | DATE | NOT NULL | Fecha de contratación |
| `city_id` | INT | NOT NULL, FK | Ciudad de ubicación de trabajo |
| `manager_id` | INT | NULL, FK | Referencia al jefe (auto-referencia) |
| `commission_percentage` | DECIMAL(5,2) | DEFAULT 0.00 | Porcentaje de comisión de ventas |
| `status` | ENUM | DEFAULT 'active' | Estado laboral |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Valores de Estado:**
- `active`: Actualmente empleado
- `inactive`: Despedido/renunciado
- `leave`: Con licencia

**Propósito:** Gestión de empleados y jerarquía  
**Relaciones:** 
- Padre: `users(id)`, `cities(id)`, `employees(id)` (jefe)
- Referenciada por: `customers`, `warehouses`, `purchase_orders`, `sales`, etc.

---

### 6. **customers** - Información de Clientes
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del cliente |
| `user_id` | INT | NOT NULL, UNIQUE, FK | Referencia a la tabla users |
| `customer_type` | ENUM | NOT NULL | Tipo de cliente |
| `identification_document` | VARCHAR(50) | NOT NULL | RUC, DNI o registro empresarial |
| `registration_date` | DATE | NOT NULL | Fecha de registro del cliente |
| `city_id` | INT | NOT NULL, FK | Ubicación del cliente |
| `address` | TEXT | NULL | Dirección completa |
| `credit_limit` | DECIMAL(12,2) | DEFAULT 0.00 | Límite de crédito para compras |
| `assigned_employee_id` | INT | NULL, FK | Representante de ventas asignado |
| `status` | ENUM | DEFAULT 'active' | Estado de la cuenta del cliente |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Valores de Tipo de Cliente:**
- `individual`: Persona natural
- `corporate`: Entidad empresarial

**Valores de Estado:**
- `active`: Puede realizar compras
- `inactive`: Cuenta deshabilitada
- `delinquent`: Problemas de pago

**Propósito:** Gestión de relaciones con clientes  
**Relaciones:** 
- Padre: `users(id)`, `cities(id)`, `employees(id)`
- Referenciada por: `sales`, `accounts_receivable`, `returns`

---

### 7. **suppliers** - Información de Proveedores
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del proveedor |
| `company_name` | VARCHAR(150) | NOT NULL | Razón social de la empresa |
| `tax_id` | VARCHAR(20) | NOT NULL, UNIQUE | Número de identificación tributaria |
| `email` | VARCHAR(150) | NOT NULL | Correo electrónico empresarial |
| `phone` | VARCHAR(20) | NULL | Teléfono empresarial |
| `address` | TEXT | NULL | Dirección empresarial |
| `city_id` | INT | NOT NULL, FK | Ubicación del proveedor |
| `contact_name` | VARCHAR(100) | NULL | Persona de contacto principal |
| `contact_phone` | VARCHAR(20) | NULL | Teléfono de la persona de contacto |
| `status` | ENUM | DEFAULT 'active' | Estado del proveedor |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Valores de Estado:**
- `active`: Disponible para compras
- `inactive`: No utilizado actualmente

**Propósito:** Gestión de proveedores  
**Relaciones:** 
- Padre: `cities(id)`
- Referenciada por: `products`, `purchase_orders`

---

### 8. **product_categories** - Jerarquía de Categorías de Productos
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único de la categoría |
| `name` | VARCHAR(100) | NOT NULL | Nombre de la categoría |
| `description` | TEXT | NULL | Descripción de la categoría |
| `parent_category_id` | INT | NULL, FK | Categoría padre (auto-referencia) |
| `status` | ENUM | DEFAULT 'active' | Estado de la categoría |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Valores de Estado:**
- `active`: Categoría en uso
- `inactive`: Categoría obsoleta

**Propósito:** Categorización jerárquica de productos  
**Relaciones:** 
- Auto-referencia: `product_categories(id)`
- Referenciada por: `products`

---

### 9. **products** - Datos Maestros de Productos
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del producto |
| `product_code` | VARCHAR(50) | NOT NULL, UNIQUE | Código interno del producto/SKU |
| `name` | VARCHAR(200) | NOT NULL | Nombre del producto |
| `description` | TEXT | NULL | Descripción detallada del producto |
| `category_id` | INT | NOT NULL, FK | Categoría del producto |
| `supplier_id` | INT | NOT NULL, FK | Proveedor principal |
| `purchase_price` | DECIMAL(10,2) | NOT NULL | Precio de costo del proveedor |
| `sale_price` | DECIMAL(10,2) | NOT NULL | Precio de venta al cliente |
| `current_stock` | INT | DEFAULT 0 | Cantidad actual en inventario |
| `minimum_stock` | INT | DEFAULT 0 | Umbral mínimo de stock |
| `unit_of_measure` | VARCHAR(20) | DEFAULT 'unit' | Unidad de medida |
| `weight` | DECIMAL(8,3) | NULL | Peso del producto |
| `dimensions` | VARCHAR(100) | NULL | Dimensiones del producto |
| `status` | ENUM | DEFAULT 'active' | Estado del producto |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |
| `updated_at` | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Marca de tiempo de última actualización |

**Valores de Estado:**
- `active`: Disponible para venta
- `discontinued`: Ya no disponible
- `out_of_stock`: Temporalmente no disponible

**Ejemplos de Unidad de Medida:**
- `unit` (unidad), `kilogram` (kilogramo), `liter` (litro), `meter` (metro), `box` (caja), `package` (paquete)

**Propósito:** Gestión completa de información de productos  
**Relaciones:** 
- Padre: `product_categories(id)`, `suppliers(id)`
- Referenciada por: Múltiples tablas para transacciones

---

### 10. **warehouses** - Gestión de Almacenes/Ubicaciones
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del almacén |
| `name` | VARCHAR(100) | NOT NULL | Nombre del almacén |
| `address` | TEXT | NOT NULL | Dirección completa del almacén |
| `city_id` | INT | NOT NULL, FK | Ubicación del almacén |
| `phone` | VARCHAR(20) | NULL | Número de contacto del almacén |
| `max_capacity` | INT | NULL | Capacidad máxima de almacenamiento |
| `manager_employee_id` | INT | NULL, FK | Gerente del almacén |
| `status` | ENUM | DEFAULT 'active' | Estado operacional del almacén |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Valores de Estado:**
- `active`: Operativo
- `inactive`: Cerrado
- `maintenance`: En mantenimiento

**Propósito:** Gestión de almacenes y ubicaciones de inventario  
**Relaciones:** 
- Padre: `cities(id)`, `employees(id)`
- Referenciada por: `warehouse_inventory`, `inventory_movements`

---

### 11. **warehouse_inventory** - Inventario por Ubicación
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del registro de inventario |
| `product_id` | INT | NOT NULL, FK | Referencia del producto |
| `warehouse_id` | INT | NOT NULL, FK | Ubicación del almacén |
| `quantity` | INT | NOT NULL, DEFAULT 0 | Cantidad actual en la ubicación |
| `location` | VARCHAR(50) | NULL | Ubicación específica dentro del almacén |
| `last_movement_date` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Último movimiento de inventario |

**Restricciones Únicas:**
- `uk_product_warehouse (product_id, warehouse_id)`: Un registro por producto por almacén

**Propósito:** Rastrear cantidades de inventario por ubicación de almacén  
**Relaciones:** 
- Padre: `products(id)`, `warehouses(id)`
- Relacionada con: `inventory_movements`

---

### 12. **purchase_orders** - Órdenes de Compra a Proveedores
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único de la orden de compra |
| `order_number` | VARCHAR(50) | NOT NULL, UNIQUE | Número de orden legible |
| `supplier_id` | INT | NOT NULL, FK | Referencia del proveedor |
| `requesting_employee_id` | INT | NOT NULL, FK | Empleado que creó la orden |
| `order_date` | DATE | NOT NULL | Fecha en que se realizó la orden |
| `estimated_delivery_date` | DATE | NULL | Fecha esperada de entrega |
| `actual_delivery_date` | DATE | NULL | Fecha real de entrega |
| `subtotal` | DECIMAL(12,2) | NOT NULL | Subtotal de la orden antes de impuestos |
| `taxes` | DECIMAL(12,2) | NOT NULL | Monto de impuestos |
| `total` | DECIMAL(12,2) | NOT NULL | Monto total de la orden |
| `status` | ENUM | DEFAULT 'pending' | Estado de la orden |
| `notes` | TEXT | NULL | Notas adicionales |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Valores de Estado:**
- `pending`: Esperando aprobación
- `approved`: Aprobada y enviada al proveedor
- `shipped`: En tránsito
- `received`: Entregada y recibida
- `cancelled`: Orden cancelada

**Propósito:** Gestión y seguimiento de órdenes de compra  
**Relaciones:** 
- Padre: `suppliers(id)`, `employees(id)`
- Hijo: `purchase_order_details`

---

### 13. **purchase_order_details** - Líneas de Artículos de Órdenes de Compra
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único de la línea de detalle |
| `purchase_order_id` | INT | NOT NULL, FK | Referencia de la orden de compra |
| `product_id` | INT | NOT NULL, FK | Producto que se está ordenando |
| `quantity` | INT | NOT NULL | Cantidad ordenada |
| `unit_price` | DECIMAL(10,2) | NOT NULL | Precio por unidad |
| `subtotal` | DECIMAL(12,2) | NOT NULL | Total de la línea (cantidad × precio_unitario) |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Propósito:** Artículos individuales para órdenes de compra  
**Relaciones:** 
- Padre: `purchase_orders(id)`, `products(id)`
- Eliminación en cascada con orden de compra

---

### 14. **sales** - Transacciones de Ventas
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único de la venta |
| `sale_number` | VARCHAR(50) | NOT NULL, UNIQUE | Número de venta legible |
| `customer_id` | INT | NOT NULL, FK | Cliente que realizó la compra |
| `salesperson_employee_id` | INT | NOT NULL, FK | Empleado de ventas |
| `sale_date` | DATETIME | NOT NULL | Fecha y hora de la venta |
| `subtotal` | DECIMAL(12,2) | NOT NULL | Subtotal de la venta antes de descuentos/impuestos |
| `discount` | DECIMAL(12,2) | DEFAULT 0.00 | Monto total de descuento |
| `taxes` | DECIMAL(12,2) | NOT NULL | Monto de impuestos |
| `total` | DECIMAL(12,2) | NOT NULL | Total final de la venta |
| `payment_method` | ENUM | NOT NULL | Cómo pagó el cliente |
| `status` | ENUM | DEFAULT 'completed' | Estado de la venta |
| `notes` | TEXT | NULL | Notas adicionales de la venta |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Valores de Método de Pago:**
- `cash`: Pago en efectivo
- `credit_card`: Tarjeta de crédito
- `debit_card`: Tarjeta de débito
- `transfer`: Transferencia bancaria
- `credit`: Crédito de tienda/cuenta

**Valores de Estado:**
- `pending`: Venta no finalizada
- `completed`: Venta completada exitosamente
- `cancelled`: Venta cancelada
- `returned`: Venta devuelta

**Propósito:** Registro principal de transacciones de ventas  
**Relaciones:** 
- Padre: `customers(id)`, `employees(id)`
- Hijo: `sale_details`
- Referenciada por: `accounts_receivable`, `returns`

---

### 15. **sale_details** - Líneas de Artículos de Transacciones de Ventas
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del detalle de venta |
| `sale_id` | INT | NOT NULL, FK | Referencia de la transacción de venta |
| `product_id` | INT | NOT NULL, FK | Producto vendido |
| `quantity` | INT | NOT NULL | Cantidad vendida |
| `unit_price` | DECIMAL(10,2) | NOT NULL | Precio por unidad al momento de la venta |
| `unit_discount` | DECIMAL(10,2) | DEFAULT 0.00 | Descuento por unidad |
| `subtotal` | DECIMAL(12,2) | NOT NULL | Total de la línea después de descuentos |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Propósito:** Artículos individuales para cada venta  
**Relaciones:** 
- Padre: `sales(id)`, `products(id)`
- Eliminación en cascada con venta

---

### 16. **inventory_movements** - Seguimiento de Movimientos de Inventario
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del movimiento |
| `product_id` | INT | NOT NULL, FK | Producto que se está moviendo |
| `warehouse_id` | INT | NOT NULL, FK | Ubicación del almacén |
| `movement_type` | ENUM | NOT NULL | Tipo de movimiento |
| `quantity` | INT | NOT NULL | Cantidad movida (positiva/negativa) |
| `reference_type` | ENUM | NOT NULL | Qué causó el movimiento |
| `reference_id` | INT | NULL | ID de la transacción causante |
| `employee_id` | INT | NOT NULL, FK | Empleado que registró el movimiento |
| `notes` | TEXT | NULL | Notas del movimiento |
| `movement_date` | DATETIME | DEFAULT CURRENT_TIMESTAMP | Cuándo ocurrió el movimiento |

**Valores de Tipo de Movimiento:**
- `in`: Stock entrante (aumento)
- `out`: Stock saliente (disminución)
- `adjustment`: Ajuste de inventario
- `transfer`: Transferencia entre ubicaciones

**Valores de Tipo de Referencia:**
- `sale`: Movimiento debido a venta
- `purchase`: Movimiento debido a compra
- `adjustment`: Ajuste manual
- `transfer`: Transferencia entre almacenes

**Propósito:** Pista de auditoría completa de movimientos de inventario  
**Relaciones:** 
- Padre: `products(id)`, `warehouses(id)`, `employees(id)`

---

### 17. **accounts_receivable** - Gestión de Créditos de Clientes
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único de la cuenta por cobrar |
| `sale_id` | INT | NOT NULL, FK | Transacción de venta relacionada |
| `customer_id` | INT | NOT NULL, FK | Cliente que debe dinero |
| `total_amount` | DECIMAL(12,2) | NOT NULL | Monto original adeudado |
| `pending_amount` | DECIMAL(12,2) | NOT NULL | Monto actual aún adeudado |
| `due_date` | DATE | NOT NULL | Fecha de vencimiento del pago |
| `days_overdue` | INT | DEFAULT 0 | Días pasados de la fecha de vencimiento |
| `status` | ENUM | DEFAULT 'pending' | Estado del pago |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |
| `updated_at` | TIMESTAMP | ON UPDATE CURRENT_TIMESTAMP | Marca de tiempo de última actualización |

**Valores de Estado:**
- `pending`: Pago debido, no vencido
- `paid`: Completamente pagado
- `overdue`: Pasado de la fecha de vencimiento
- `partial`: Parcialmente pagado

**Propósito:** Rastrear crédito de clientes y obligaciones de pago  
**Relaciones:** 
- Padre: `sales(id)`, `customers(id)`
- Referenciada por: `payments_received`

---

### 18. **payments_received** - Registros de Pagos de Clientes
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del pago |
| `accounts_receivable_id` | INT | NOT NULL, FK | Cuenta por cobrar relacionada |
| `payment_amount` | DECIMAL(12,2) | NOT NULL | Monto de este pago |
| `payment_method` | ENUM | NOT NULL | Cómo se realizó el pago |
| `reference_number` | VARCHAR(100) | NULL | Número de cheque, ID de transacción, etc. |
| `payment_date` | DATETIME | NOT NULL | Cuándo se recibió el pago |
| `receiving_employee_id` | INT | NOT NULL, FK | Empleado que procesó el pago |
| `notes` | TEXT | NULL | Notas del pago |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Valores de Método de Pago:**
- `cash`: Pago en efectivo
- `credit_card`: Tarjeta de crédito
- `debit_card`: Tarjeta de débito
- `transfer`: Transferencia bancaria
- `check`: Cheque en papel

**Propósito:** Registrar todos los pagos de clientes contra saldos pendientes  
**Relaciones:** 
- Padre: `accounts_receivable(id)`, `employees(id)`

---

### 19. **returns** - Solicitudes de Devolución de Productos
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único de la devolución |
| `return_number` | VARCHAR(50) | NOT NULL, UNIQUE | Número de devolución legible |
| `sale_id` | INT | NOT NULL, FK | Venta original que se está devolviendo |
| `customer_id` | INT | NOT NULL, FK | Cliente que hace la devolución |
| `authorizing_employee_id` | INT | NOT NULL, FK | Empleado que autoriza la devolución |
| `return_date` | DATETIME | NOT NULL | Cuándo se procesó la devolución |
| `reason` | TEXT | NOT NULL | Razón para la devolución |
| `total_returned` | DECIMAL(12,2) | NOT NULL | Valor total que se devuelve |
| `status` | ENUM | DEFAULT 'pending' | Estado de la devolución |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Valores de Estado:**
- `pending`: Solicitud de devolución enviada
- `approved`: Devolución aprobada
- `rejected`: Devolución denegada
- `processed`: Devolución completada y procesada

**Razones Comunes de Devolución:**
- Producto defectuoso
- No cumple con las expectativas
- Llegó dañado
- Orden incorrecta
- El cliente cambió de opinión
- Reclamo de garantía
- Error de ventas

**Propósito:** Gestionar devoluciones de productos y reembolsos  
**Relaciones:** 
- Padre: `sales(id)`, `customers(id)`, `employees(id)`
- Hijo: `return_details`

---

### 20. **return_details** - Líneas de Artículos de Devoluciones
| Columna | Tipo | Restricciones | Descripción |
|---------|------|---------------|-------------|
| `id` | INT | PRIMARY KEY, AUTO_INCREMENT | Identificador único del detalle de devolución |
| `return_id` | INT | NOT NULL, FK | Referencia de la transacción de devolución |
| `product_id` | INT | NOT NULL, FK | Producto que se está devolviendo |
| `quantity_returned` | INT | NOT NULL | Cuántas unidades se devolvieron |
| `unit_price` | DECIMAL(10,2) | NOT NULL | Precio unitario original |
| `subtotal_returned` | DECIMAL(12,2) | NOT NULL | Valor total para esta línea |
| `product_condition` | ENUM | NOT NULL | Condición del producto devuelto |
| `created_at` | TIMESTAMP | DEFAULT CURRENT_TIMESTAMP | Marca de tiempo de creación del registro |

**Valores de Condición del Producto:**
- `new`: Producto en condición nueva
- `used`: Producto muestra signos de uso
- `damaged`: Producto está dañado

**Propósito:** Artículos individuales para cada transacción de devolución  
**Relaciones:** 
- Padre: `returns(id)`, `products(id)`
- Eliminación en cascada con devolución

---

## Índices de Base de Datos para Rendimiento

### Índices Primarios (Automáticos)
- Todas las columnas `id` tienen índices de clave primaria

### Índices Adicionales
- `idx_sales_date`: Índice en `sales.sale_date` para consultas de rango de fechas
- `idx_sales_customer`: Índice en `sales.customer_id` para búsqueda de clientes
- `idx_sales_employee`: Índice en `sales.salesperson_employee_id` para rendimiento de empleados
- `idx_products_category`: Índice en `products.category_id` para filtrado de categorías
- `idx_movements_date`: Índice en `inventory_movements.movement_date` para seguimiento de movimientos
- `idx_accounts_due_date`: Índice en `accounts_receivable.due_date` para seguimiento de pagos

---

## Reglas de Negocio y Restricciones

### Integridad de Datos
1. **Restricciones Únicas**: Direcciones de correo electrónico, códigos de empleados, códigos de productos, números de orden
2. **Restricciones de Clave Foránea**: Todas las relaciones aplicadas a nivel de base de datos
3. **Restricciones Enum**: Campos de estado limitados a valores predefinidos
4. **Restricciones Not Null**: Campos esenciales no pueden estar vacíos

### Lógica de Negocio
1. **Datos Jerárquicos**: Categorías y gestión de empleados soportan relaciones padre-hijo
2. **Precisión Financiera**: Todos los cálculos monetarios usan DECIMAL para precisión
3. **Pista de Auditoría**: Marcas de tiempo de creación/actualización en tablas clave
4. **Gestión de Estado**: Enums de estado consistentes en tablas relacionadas

### Reglas de Validación Recomendadas
1. **Formato de Correo Electrónico**: Validar formato de correo electrónico antes de inserción
2. **Valores Positivos**: Cantidades, precios y montos deben ser positivos
3. **Lógica de Fechas**: Fechas de vencimiento deben ser posteriores a fechas de venta, fechas de entrega posteriores a fechas de orden
4. **Validación de Stock**: Cantidades de ventas no deben exceder el stock disponible
5. **Límites de Crédito**: Las compras de clientes deben respetar los límites de crédito

---

## Ejemplos de Uso

### Consultas Comunes

**Encontrar todos los productos activos en la categoría Electrónicos:**
```sql
SELECT p.* FROM products p
JOIN product_categories pc ON p.category_id = pc.id
WHERE pc.name LIKE '%Electronics%' AND p.status = 'active';
```

**Resumen de ventas de clientes:**
```sql
SELECT c.user_id, u.first_name, u.last_name, 
       COUNT(s.id) as total_ventas, SUM(s.total) as monto_total
FROM customers c
JOIN users u ON c.user_id = u.id
JOIN sales s ON c.id = s.customer_id
WHERE s.status = 'completed'
GROUP BY c.id;
```

**Cuentas vencidas:**
```sql
SELECT ar.*, c.user_id, u.first_name, u.last_name
FROM accounts_receivable ar
JOIN customers c ON ar.customer_id = c.id
JOIN users u ON c.user_id = u.id
WHERE ar.status IN ('overdue', 'partial') AND ar.days_overdue > 0;
```

---

Este diccionario de datos proporciona una referencia completa para entender y trabajar con la estructura de la base de datos del sistema de ventas.
