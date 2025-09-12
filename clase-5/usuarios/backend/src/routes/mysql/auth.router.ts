import { Router } from 'express';
import { AuthController } from '../../controllers/mysql/auth.controller';
import authMiddleware from '../../middleware/auth.middleware';

const router = Router();
const authController = new AuthController();

// Rutas públicas
router.post('/auth/login', authController.login);

// Rutas protegidas (requieren autenticación)
router.get('/auth/verify', authMiddleware, authController.verifyToken);

export default router;
