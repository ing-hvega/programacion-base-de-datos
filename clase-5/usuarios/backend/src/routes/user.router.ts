import {Router} from "express";
import {createUser, getUsers} from "../controllers/user.controller";
import authMiddleware from "../middleware/auth.middleware";

const router = Router()

router.post('/user', createUser)
router.get('/users', getUsers)

export default router