import {Router} from "express";
import {createUser, getUsers} from "../controllers/user.controller";
import authMiddleware from "../middleware/auth.middleware";

const router = Router()

router.post('/user', authMiddleware, createUser)
router.get('/users', authMiddleware, getUsers)

export default router