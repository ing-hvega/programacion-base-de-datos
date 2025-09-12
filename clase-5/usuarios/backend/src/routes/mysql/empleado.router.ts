import { Router } from "express";
import authMiddleware from "../../middleware/auth.middleware";
import { EmpleadoControllerORM } from "../../controllers/mysql/empleado.controller.orm";

const router = Router();
const empleadoController = new EmpleadoControllerORM();

// Rutas públicas (sin autenticación)
router.get('/empleado/:id', authMiddleware, empleadoController.getEmpleadoById);
router.get('/empleados', authMiddleware, empleadoController.getEmpleados);
router.get('/empleados/departamentos', authMiddleware, empleadoController.getDepartamentos);
router.get('/empleados/cargos', authMiddleware, empleadoController.getCargos);

// Rutas protegidas (requieren autenticación)
router.post('/empleado', authMiddleware, empleadoController.createEmpleado);
router.put('/empleado/:id', authMiddleware, empleadoController.updateEmpleado);
router.delete('/empleado/:id', authMiddleware, empleadoController.deleteEmpleado);

export default router;
