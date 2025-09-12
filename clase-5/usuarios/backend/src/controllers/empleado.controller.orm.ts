import { Request, Response } from 'express';
import { getRepository } from 'typeorm';
import { EmpleadoEntity } from '../models/empleado.entity';
import { CrearEmpleadoDTO, ActualizarEmpleadoDTO, EmpleadoFiltros } from '../models/empleado.model';

export class EmpleadoControllerORM {
  /**
   * Crea un nuevo empleado con verificación de duplicados usando TypeORM
   */
  async createEmpleado(req: Request, res: Response): Promise<void> {
    try {
      const empleadoData: CrearEmpleadoDTO = req.body;
      const empleadoRepository = getRepository(EmpleadoEntity);

      // Validaciones básicas
      if (!empleadoData.nombre) {
        res.status(400).json({
          success: false,
          message: 'Faltan campos requeridos'
        });
        return;
      }

      // Verificar si ya existe un empleado con el mismo email o DNI
      const verificacion = await empleadoRepository.count({
        where: [
          { email: empleadoData.email },
          { dni: empleadoData.dni }
        ]
      });

      if (verificacion > 0) {
        res.status(409).json({
          success: false,
          message: 'Ya existe un empleado con el mismo email o DNI'
        });
        return;
      }

      // Transformar el DTO a la entidad
      const nuevoEmpleado = empleadoRepository.create({
        ...empleadoData,
        fechaContratacion: empleadoData.fecha_contratacion,
        estado: empleadoData.estado || 'activo'
      });

      const empleadoGuardado = await empleadoRepository.save(nuevoEmpleado);

      res.status(201).json({
        success: true,
        message: 'Empleado creado exitosamente',
        data: empleadoGuardado
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: 'Error al crear el empleado',
        error: error.message
      });
    }
  }

  /**
   * Actualiza un empleado existente con verificación de duplicados
   */
  async updateEmpleado(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const empleadoData: ActualizarEmpleadoDTO = req.body;
      const empleadoRepository = getRepository(EmpleadoEntity);

      if (Object.keys(empleadoData).length === 0) {
        res.status(400).json({
          success: false,
          message: 'No se proporcionaron datos para actualizar'
        });
        return;
      }

      // Verificar que el empleado existe
      const empleadoExistente = await empleadoRepository.findOne({ where: { id: Number(id) } });

      if (!empleadoExistente) {
        res.status(404).json({
          success: false,
          message: `No se encontró empleado con ID ${id}`
        });
        return;
      }

      // Verificar duplicados si se actualiza email o DNI
      if (empleadoData.email || empleadoData.dni) {
        // Usando QueryBuilder para una consulta más compleja
        const queryBuilder = empleadoRepository.createQueryBuilder('empleado')
          .where('empleado.id != :id', { id });

        if (empleadoData.email) {
          queryBuilder.andWhere('empleado.email = :email', { email: empleadoData.email });
        }

        if (empleadoData.dni) {
          queryBuilder.orWhere('empleado.dni = :dni', { dni: empleadoData.dni });
        }

        const verificacion = await queryBuilder.getCount();

        if (verificacion > 0) {
          res.status(409).json({
            success: false,
            message: 'El email o DNI ya está en uso por otro empleado'
          });
          return;
        }
      }

      // Transformar el DTO para actualizar la entidad
      const datosParaActualizar: Partial<EmpleadoEntity> = {
        ...empleadoData,
        fechaContratacion: empleadoData.fecha_contratacion
      };

      // Actualizar el empleado
      await empleadoRepository.update(id, datosParaActualizar);

      // Obtener el empleado actualizado
      const empleadoActualizado = await empleadoRepository.findOne({ where: { id: Number(id) } });

      res.status(200).json({
        success: true,
        message: 'Empleado actualizado exitosamente',
        data: empleadoActualizado
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: 'Error al actualizar el empleado',
        error: error.message
      });
    }
  }

  /**
   * Obtiene un empleado por ID
   */
  async getEmpleadoById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const empleadoRepository = getRepository(EmpleadoEntity);

      const empleado = await empleadoRepository.findOne({ where: { id: Number(id) } });

      if (!empleado) {
        res.status(404).json({
          success: false,
          message: `No se encontró empleado con ID ${id}`
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: empleado
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: 'Error al obtener el empleado',
        error: error.message
      });
    }
  }

  /**
   * Elimina un empleado por ID
   */
  async deleteEmpleado(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const empleadoRepository = getRepository(EmpleadoEntity);

      const empleado = await empleadoRepository.findOne({ where: { id: Number(id) } });

      if (!empleado) {
        res.status(404).json({
          success: false,
          message: `No se encontró empleado con ID ${id}`
        });
        return;
      }

      await empleadoRepository.delete(id);

      res.status(200).json({
        success: true,
        message: 'Empleado eliminado exitosamente'
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: 'Error al eliminar el empleado',
        error: error.message
      });
    }
  }

  /**
   * Obtiene todos los empleados con filtros opcionales
   */
  async getEmpleados(req: Request, res: Response): Promise<void> {
    try {
      const filtros: EmpleadoFiltros = req.query as any;
      const empleadoRepository = getRepository(EmpleadoEntity);

      // Crear el query builder para aplicar filtros
      const queryBuilder = empleadoRepository.createQueryBuilder('empleado');

      // Aplicar filtros
      if (filtros.departamento) {
        queryBuilder.andWhere('empleado.departamento = :departamento', {
          departamento: filtros.departamento
        });
      }

      if (filtros.cargo) {
        queryBuilder.andWhere('empleado.cargo = :cargo', {
          cargo: filtros.cargo
        });
      }

      if (filtros.estado) {
        queryBuilder.andWhere('empleado.estado = :estado', {
          estado: filtros.estado
        });
      }

      if (filtros.busqueda) {
        queryBuilder.andWhere(
          '(empleado.nombre LIKE :busqueda OR empleado.apellido LIKE :busqueda OR empleado.email LIKE :busqueda OR empleado.dni LIKE :busqueda)',
          { busqueda: `%${filtros.busqueda}%` }
        );
      }

      // Ordenar resultados
      queryBuilder.orderBy('empleado.apellido', 'ASC').addOrderBy('empleado.nombre', 'ASC');

      // Ejecutar consulta
      const empleados = await queryBuilder.getMany();

      res.status(200).json({
        success: true,
        data: empleados
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: 'Error al obtener los empleados',
        error: error.message
      });
    }
  }

  /**
   * Obtiene los departamentos disponibles
   */
  async getDepartamentos(req: Request, res: Response): Promise<void> {
    try {
      const empleadoRepository = getRepository(EmpleadoEntity);

      const departamentos = await empleadoRepository
        .createQueryBuilder('empleado')
        .select('DISTINCT empleado.departamento', 'departamento')
        .orderBy('empleado.departamento', 'ASC')
        .getRawMany();

      res.status(200).json({
        success: true,
        data: departamentos.map(item => item.departamento).filter(Boolean)
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: 'Error al obtener los departamentos',
        error: error.message
      });
    }
  }

  /**
   * Obtiene los cargos disponibles
   */
  async getCargos(req: Request, res: Response): Promise<void> {
    try {
      const empleadoRepository = getRepository(EmpleadoEntity);

      const cargos = await empleadoRepository
        .createQueryBuilder('empleado')
        .select('DISTINCT empleado.cargo', 'cargo')
        .orderBy('empleado.cargo', 'ASC')
        .getRawMany();

      res.status(200).json({
        success: true,
        data: cargos.map(item => item.cargo).filter(Boolean)
      });
    } catch (error: any) {
      res.status(500).json({
        success: false,
        message: 'Error al obtener los cargos',
        error: error.message
      });
    }
  }
}
