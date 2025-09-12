import { Router } from 'express';
import { EmpleadoController } from '../controllers/empleado.controller';
import authMiddleware from "../middleware/auth.middleware";
import {EmpleadoControllerORM} from "../controllers/empleado.controller.orm";

const router = Router();
const empleadoController = new EmpleadoControllerORM();

router.get('/:id', authMiddleware, empleadoController.getEmpleadoById);

router.put('/:id', authMiddleware, empleadoController.updateEmpleado);

router.delete('/:id', authMiddleware, empleadoController.deleteEmpleado);

router.post('/', authMiddleware, empleadoController.createEmpleado);

export default router;
