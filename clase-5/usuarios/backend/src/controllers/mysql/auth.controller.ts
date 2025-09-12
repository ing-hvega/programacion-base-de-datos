import { Request, Response } from 'express';
import bcrypt from 'bcrypt';
import jwt from 'jsonwebtoken';
import { getDataSource } from "../../config/typeorm.config";
import { UserEntity } from '../../models/mysql/user.entity';
import { LoginDTO } from '../../dto/user.model';

export class AuthController {
  /**
   * Autenticación de usuario (login)
   */
  async login(req: Request, res: Response): Promise<void> {
    try {
      const loginData: LoginDTO = req.body;
      const dataSource = await getDataSource()
      const userRepository = dataSource.getRepository(UserEntity);

      // Validar que se proporcione email y password
      if (!loginData.email || !loginData.password) {
        res.status(400).json({
          success: false,
          message: 'Se requieren email y contraseña para iniciar sesión'
        });
        return;
      }

      // Buscar el usuario por email
      const user = await userRepository.findOne({
        where: { email: loginData.email }
      });

      // Verificar si el usuario existe
      if (!user) {
        res.status(401).json({
          success: false,
          message: 'Credenciales inválidas'
        });
        return;
      }

      // Verificar si el usuario está activo
      if (!user.active) {
        res.status(403).json({
          success: false,
          message: 'Usuario desactivado. Contacte al administrador'
        });
        return;
      }

      // Comparar la contraseña proporcionada con la almacenada
      const isPasswordValid = await bcrypt.compare(loginData.password, user.password);
      if (!isPasswordValid) {
        res.status(401).json({
          success: false,
          message: 'Credenciales inválidas'
        });
        return;
      }

      // Generar el token JWT
      const token = jwt.sign(
        {
          userId: user.id,
          email: user.email,
          role: user.role
        },
        process.env.JWT_SECRET || 'your_jwt_secret',
        { expiresIn: '24h' }
      );

      // Excluir la contraseña de la respuesta
      const { password, ...userResponse } = user;

      res.status(200).json({
        success: true,
        message: 'Inicio de sesión exitoso',
        data: {
          token,
          user: userResponse
        }
      });
    } catch (error: any) {
      console.error('Error en login:', error);
      res.status(500).json({
        success: false,
        message: 'Error al iniciar sesión',
        error: error.message
      });
    }
  }

  /**
   * Verifica el token JWT y devuelve la información del usuario
   */
  async verifyToken(req: Request, res: Response): Promise<void> {
    try {
      // El middleware de autenticación ya valida el token y añade el usuario a req
      const userId = (req as any).user?.userId;

      if (!userId) {
        res.status(401).json({
          success: false,
          message: 'Token inválido o expirado'
        });
        return;
      }

      const dataSource = await getDataSource();
      const userRepository = dataSource.getRepository(UserEntity);

      const user = await userRepository.findOne({
        where: { id: userId },
        select: ['id', 'nombre', 'apellido', 'email', 'role', 'active', 'createdAt', 'updatedAt']
      });

      if (!user) {
        res.status(404).json({
          success: false,
          message: 'Usuario no encontrado'
        });
        return;
      }

      res.status(200).json({
        success: true,
        data: user
      });
    } catch (error: any) {
      console.error('Error en verifyToken:', error);
      res.status(500).json({
        success: false,
        message: 'Error al verificar token',
        error: error.message
      });
    }
  }
}
