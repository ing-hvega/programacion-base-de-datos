import { Request, Response } from 'express';
import { query } from '../../config/database-mysql.config';
import { Empleado, EmpleadoFiltros, CrearEmpleadoDTO, ActualizarEmpleadoDTO } from '../../dto/empleado.model';

export class EmpleadoController {
  /**
   * Obtiene todos los empleados con filtros opcionales
   */
  async getEmpleados(req: Request, res: Response): Promise<void> {
    try {
      const filtros: EmpleadoFiltros = req.query as any;
      let sql = 'SELECT * FROM empleados WHERE 1=1';
      const params: any[] = [];

      // Aplicar filtros
      if (filtros.departamento) {
        sql += ' AND departamento = ?';
        params.push(filtros.departamento);
      }

      if (filtros.cargo) {
        sql += ' AND cargo = ?';
        params.push(filtros.cargo);
      }

      if (filtros.estado) {
        sql += ' AND estado = ?';
        params.push(filtros.estado);
      }

      if (filtros.busqueda) {
        sql += ' AND (nombre LIKE ? OR apellido LIKE ? OR email LIKE ? OR dni LIKE ?)';
        const termino = `%${filtros.busqueda}%`;
        params.push(termino, termino, termino, termino);
      }

      sql += ' ORDER BY apellido, nombre';

      const empleados = await query(sql, params) as Empleado[];
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
   * Obtiene un empleado por su ID
   */
  async getEmpleadoById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const sql = 'SELECT * FROM empleados WHERE id = ?';
      const empleados = await query(sql, [id]) as Empleado[];

      if (empleados.length === 0) {
        res.status(404).json({
          success: false,
          message: `No se encontró empleado con ID ${id}`
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: empleados[0]
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
   * Crea un nuevo empleado
   */
  async createEmpleado(req: Request, res: Response): Promise<void> {
    try {
      const empleadoData: CrearEmpleadoDTO = req.body;

      // Validaciones básicas
      if (!empleadoData.nombre) {
        res.status(400).json({
          success: false,
          message: 'Faltan campos requeridos'
        });
        return;
      }

      // Verificar si ya existe un empleado con el mismo email o DNI
      const verificacion = await query(
        'SELECT COUNT(*) as count FROM empleados WHERE email = ? OR dni = ?',
        [empleadoData.email, empleadoData.dni]
      ) as any[];

      if (verificacion[0].count > 0) {
        res.status(409).json({
          success: false,
          message: 'Ya existe un empleado con el mismo email o DNI'
        });
        return;
      }

      // Preparar la consulta SQL
      const campos = Object.keys(empleadoData).join(', ');
      const placeholders = Object.keys(empleadoData).map(() => '?').join(', ');
      const valores = Object.values(empleadoData);

      const sql = `INSERT INTO empleados (${campos}) VALUES (${placeholders})`;
      const resultado = await query(sql, valores) as any;

      res.status(201).json({
        success: true,
        message: 'Empleado creado exitosamente',
        data: {
          id: resultado.insertId,
          ...empleadoData
        }
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
   * Actualiza un empleado existente
   */
  async updateEmpleado(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const empleadoData: ActualizarEmpleadoDTO = req.body;

      if (Object.keys(empleadoData).length === 0) {
        res.status(400).json({
          success: false,
          message: 'No se proporcionaron datos para actualizar'
        });
        return;
      }

      // Verificar que el empleado existe
      const empleadoExistente = await query('SELECT * FROM empleados WHERE id = ?', [id]) as Empleado[];

      if (empleadoExistente.length === 0) {
        res.status(404).json({
          success: false,
          message: `No se encontró empleado con ID ${id}`
        });
        return;
      }

      // Verificar duplicados si se actualiza email o DNI
      if (empleadoData.email || empleadoData.dni) {
        let checkSql = 'SELECT COUNT(*) as count FROM empleados WHERE id != ? AND (';
        const checkParams: any[] = [id];

        if (empleadoData.email) {
          checkSql += 'email = ?';
          checkParams.push(empleadoData.email);
        }

        if (empleadoData.dni) {
          if (empleadoData.email) checkSql += ' OR ';
          checkSql += 'dni = ?';
          checkParams.push(empleadoData.dni);
        }

        checkSql += ')';

        const verificacion = await query(checkSql, checkParams) as any[];

        if (verificacion[0].count > 0) {
          res.status(409).json({
            success: false,
            message: 'El email o DNI ya está en uso por otro empleado'
          });
          return;
        }
      }

      // Preparar la actualización
      const updatePairs = Object.keys(empleadoData).map(key => `${key} = ?`).join(', ');
      const updateParams = [...Object.values(empleadoData), id];

      const sql = `UPDATE empleados SET ${updatePairs} WHERE id = ?`;
      await query(sql, updateParams);

      res.status(200).json({
        success: true,
        message: 'Empleado actualizado exitosamente',
        data: {
          id: Number(id),
          ...empleadoExistente[0],
          ...empleadoData
        }
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
   * Elimina un empleado por su ID
   */
  async deleteEmpleado(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;

      // Verificar que el empleado existe
      const empleadoExistente = await query('SELECT * FROM empleados WHERE id = ?', [id]) as Empleado[];

      if (empleadoExistente.length === 0) {
        res.status(404).json({
          success: false,
          message: `No se encontró empleado con ID ${id}`
        });
        return;
      }

      const sql = 'DELETE FROM empleados WHERE id = ?';
      await query(sql, [id]);

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
   * Obtiene los departamentos disponibles
   */
  async getDepartamentos(req: Request, res: Response): Promise<void> {
    try {
      const sql = 'SELECT DISTINCT departamento FROM empleados ORDER BY departamento';
      const departamentos = await query(sql) as any[];

      res.status(200).json({
        success: true,
        data: departamentos.map(item => item.departamento)
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
      const sql = 'SELECT DISTINCT cargo FROM empleados ORDER BY cargo';
      const cargos = await query(sql) as any[];

      res.status(200).json({
        success: true,
        data: cargos.map(item => item.cargo)
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
