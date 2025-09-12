import {Request, Response} from "express";
import PlaneSchema from "../../models/mongodb/plane.schema";

const createPlane = async (req: Request, res: Response) => {
    try {

        const {name, version, router_file, state} = req.body

        const newPlane = new PlaneSchema({
            name,
            version,
            router_file,
            state,
            created_by: "68c0efef5a5b9a22a5ca14c2"
        })

        await newPlane.save()

        res.status(201).json({
            message: "El plano creado exitosamente",
            status: true,
        })
    } catch (e: any) {
        res.status(500).json({
            message: "Error al crear el plano",
            status: false,
        })
    }
}

const getPlanes = async (req: Request, res: Response) => {

    const response = await PlaneSchema.find({active: true}, {name: 1, version: 1, router_file: 1, state: 1})

    return res.status(200).json({
        message: "Planes obtenidos exitosamente",
        status: true,
        data: response,
    })
}

const updatePlanes = async (req: Request, res: Response) => {

    const {id} = req.params

    const existePlane = await PlaneSchema.find({'_id': id})

    if (!existePlane) {
        return res.status(404).json({
            message: "El plano no existe",
            status: false,
        })
    }

    const {name, version, state} = req.body

    const response = await PlaneSchema.updateOne({'_id': id}, {name, version, state})
    console.log(response)

    return res.status(200).json({
        message: "Planes actualizados exitosamente",
        status: true,
        data: response,
    })
}

const deletePlanes = async (req: Request, res: Response) => {

    const { id } = req.params


    // Eliminacion fisica
    // await PlaneSchema.deleteOne({'_id': id})

    /// Eliminación logica
    await PlaneSchema.updateOne({'_id': id}, {active: false})

    return res.status(200).json({
        message: "Plano eliminado exitosamente",
        status: true,
    })
}

const getPlanesById = async (req: Request, res: Response) => {

    const { id } = req.params

    const response = await PlaneSchema.findById(id)

    return res.status(200).json({
        message: "Plan obtenido exitosamente",
        status: true,
        data: response,
    })
}


export {createPlane, getPlanes, updatePlanes, deletePlanes, getPlanesById}