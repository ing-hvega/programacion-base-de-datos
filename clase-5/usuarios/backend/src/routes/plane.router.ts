import {Router} from "express";
import {createPlane, getPlanes} from "../controllers/plane.controller";


const router = Router()

router.post('/plane', createPlane)
router.get('/planes', getPlanes)

export default router