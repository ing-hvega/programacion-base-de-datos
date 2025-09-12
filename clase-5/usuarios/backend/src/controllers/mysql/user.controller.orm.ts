import { Request, Response } from 'express';
import { UserEntity } from '../../models/mysql/user.entity';
import { CreateUserDTO, UpdateUserDTO } from '../../dto/user.model';
import { getDataSource } from '../../config/typeorm.config';
import bcrypt from 'bcrypt';

export class UserController {
  /**
   * Crea un nuevo usuario
   */
  async createUser(req: Request, res: Response): Promise<void> {
    try {
      const userData: CreateUserDTO = req.body;
      const dataSource = await getDataSource();
      const userRepository = dataSource.getRepository(UserEntity);

      // Validaciones básicas
      if (!userData.nombre || !userData.email || !userData.password) {
        res.status(400).json({
          success: false,
          message: 'Faltan campos requeridos: nombre, email y password son obligatorios'
        });
        return;
      }

      // Verificar si ya existe un usuario con el mismo email
      const existingUser = await userRepository.findOne({
        where: { email: userData.email }
      });

      if (existingUser) {
        res.status(409).json({
          success: false,
          message: 'Ya existe un usuario con ese email'
        });
        return;
      }

      // Hash de la contraseña
      const hashedPassword = await bcrypt.hash(userData.password, 10);

      // Crear el nuevo usuario
      const newUser = userRepository.create({
        ...userData,
        password: hashedPassword
      });

      const savedUser = await userRepository.save(newUser);

      // Usar una doble aserción para solucionar el problema de tipo
      const { password, ...userResponse } = savedUser as unknown as { password: string } & Record<string, any>;

      res.status(201).json({
        success: true,
        message: 'Usuario creado exitosamente',
        data: userResponse
      });
    } catch (error: any) {
      console.error('Error en createUser:', error);
      res.status(500).json({
        success: false,
        message: 'Error al crear el usuario',
        error: error.message
      });
    }
  }

  /**
   * Obtiene un usuario por su ID
   */
  async getUserById(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const dataSource = await getDataSource();
      const userRepository = dataSource.getRepository(UserEntity);

      const user = await userRepository.findOne({
        where: { id: Number(id) }
      });

      if (!user) {
        res.status(404).json({
          success: false,
          message: `No se encontró usuario con ID ${id}`
        });
        return;
      }

      // Excluir la contraseña de la respuesta
      const { password, ...userResponse } = user;

      res.status(200).json({
        success: true,
        data: userResponse
      });
    } catch (error: any) {
      console.error('Error en getUserById:', error);
      res.status(500).json({
        success: false,
        message: 'Error al obtener el usuario',
        error: error.message
      });
    }
  }

  /**
   * Actualiza un usuario existente
   */
  async updateUser(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const userData: UpdateUserDTO = req.body;
      const dataSource = await getDataSource();
      const userRepository = dataSource.getRepository(UserEntity);

      if (Object.keys(userData).length === 0) {
        res.status(400).json({
          success: false,
          message: 'No se proporcionaron datos para actualizar'
        });
        return;
      }

      // Verificar que el usuario existe
      const existingUser = await userRepository.findOne({
        where: { id: Number(id) }
      });

      if (!existingUser) {
        res.status(404).json({
          success: false,
          message: `No se encontró usuario con ID ${id}`
        });
        return;
      }

      // Si se va a actualizar el email, verificar que no exista otro usuario con ese email
      if (userData.email && userData.email !== existingUser.email) {
        const duplicateEmail = await userRepository.findOne({
          where: { email: userData.email }
        });

        if (duplicateEmail) {
          res.status(409).json({
            success: false,
            message: 'Ya existe otro usuario con ese email'
          });
          return;
        }
      }

      // Si se va a actualizar la contraseña, hashearla
      if (userData.password) {
        userData.password = await bcrypt.hash(userData.password, 10);
      }

      // Actualizar el usuario
      await userRepository.update(id, userData);

      // Obtener el usuario actualizado
      const updatedUser = await userRepository.findOne({
        where: { id: Number(id) }
      });

      // Excluir la contraseña de la respuesta
      const { password, ...userResponse } = updatedUser!;

      res.status(200).json({
        success: true,
        message: 'Usuario actualizado exitosamente',
        data: userResponse
      });
    } catch (error: any) {
      console.error('Error en updateUser:', error);
      res.status(500).json({
        success: false,
        message: 'Error al actualizar el usuario',
        error: error.message
      });
    }
  }

  /**
   * Elimina un usuario
   */
  async deleteUser(req: Request, res: Response): Promise<void> {
    try {
      const { id } = req.params;
      const dataSource = await getDataSource();
      const userRepository = dataSource.getRepository(UserEntity);

      // Verificar que el usuario existe
      const existingUser = await userRepository.findOne({
        where: { id: Number(id) }
      });

      if (!existingUser) {
        res.status(404).json({
          success: false,
          message: `No se encontró usuario con ID ${id}`
        });
        return;
      }

      // Eliminar el usuario
      await userRepository.delete(id);

      res.status(200).json({
        success: true,
        message: 'Usuario eliminado exitosamente'
      });
    } catch (error: any) {
      console.error('Error en deleteUser:', error);
      res.status(500).json({
        success: false,
        message: 'Error al eliminar el usuario',
        error: error.message
      });
    }
  }

  /**
   * Obtiene todos los usuarios
   */
  async getAllUsers(req: Request, res: Response): Promise<void> {
    try {
      const dataSource = await getDataSource();
      const userRepository = dataSource.getRepository(UserEntity);
      const users = await userRepository.find({
        select: ['id', 'nombre', 'apellido', 'email', 'role', 'active', 'createdAt', 'updatedAt']
      });

      res.status(200).json({
        success: true,
        data: users
      });
    } catch (error: any) {
      console.error('Error en getAllUsers:', error);
      res.status(500).json({
        success: false,
        message: 'Error al obtener los usuarios',
        error: error.message
      });
    }
  }
}
