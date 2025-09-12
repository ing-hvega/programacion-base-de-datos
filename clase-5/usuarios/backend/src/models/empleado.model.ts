import { RowDataPacket } from 'mysql2';

// Interfaz para el modelo de Empleado
export interface Empleado extends RowDataPacket {
  id?: number;
  nombre: string;
  apellido: string;
  email: string;
  cargo: string;
  departamento: string;
  salario: number;
  fecha_contratacion: Date;
  telefono?: string;
  direccion?: string;
  dni: string;
  estado?: 'activo' | 'inactivo' | 'suspendido';
  fecha_creacion?: Date;
  fecha_actualizacion?: Date;
}

// Interfaz para filtros de búsqueda de empleados
export interface EmpleadoFiltros {
  departamento?: string;
  cargo?: string;
  estado?: 'activo' | 'inactivo' | 'suspendido';
  busqueda?: string;
}

// Interfaz para la creación de un empleado (omitiendo campos opcionales y generados)
export interface CrearEmpleadoDTO {
  nombre: string;
  apellido: string;
  email: string;
  cargo: string;
  departamento: string;
  salario: number;
  fecha_contratacion: Date;
  telefono?: string;
  direccion?: string;
  dni: string;
  estado?: 'activo' | 'inactivo' | 'suspendido';
}

// Interfaz para actualizar un empleado (todos los campos son opcionales)
export interface ActualizarEmpleadoDTO {
  nombre?: string;
  apellido?: string;
  email?: string;
  cargo?: string;
  departamento?: string;
  salario?: number;
  fecha_contratacion?: Date;
  telefono?: string;
  direccion?: string;
  dni?: string;
  estado?: 'activo' | 'inactivo' | 'suspendido';
}
