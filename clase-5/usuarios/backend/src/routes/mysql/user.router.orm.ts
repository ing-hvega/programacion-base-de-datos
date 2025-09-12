import { Router } from 'express';
import { UserController } from '../../controllers/mysql/user.controller.orm';
import authMiddleware from '../../middleware/auth.middleware';

const router = Router();
const userController = new UserController();

// Rutas públicas
router.post('/users/register', userController.createUser);

// Rutas protegidas (requieren autenticación)
router.get('/users', authMiddleware, userController.getAllUsers);
router.get('/users/:id', authMiddleware, userController.getUserById);
router.put('/users/:id', authMiddleware, userController.updateUser);
router.delete('/users/:id', authMiddleware, userController.deleteUser);

export default router;
