import {Router} from "express";
import {createPlane, deletePlanes, getPlanes, getPlanesById, updatePlanes} from "../../controllers/mongodb/planes.controller";

const router = Router()

router.post('/plane', createPlane)
router.get('/planes', getPlanes)
router.put('/plane/:id', updatePlanes)
router.delete('/plane/:id', deletePlanes)
router.get('/plane/:id', getPlanesById)

export default router