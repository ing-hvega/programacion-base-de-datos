import {Router} from "express";
import {createUser, getUsers} from "../../controllers/mongodb/user.controller";

const router = Router()

router.post('/user', createUser)
router.get('/users', getUsers)

export default router