import {Request, Response} from "express";
import PlaneSchema from "../models/plane.schema";

const createPlane = async (req: Request, res: Response)=> {
        try {

            const {name, version, router_file, state }= req.body

            const newPlane = new PlaneSchema({
                name,
                version,
                router_file,
                state,
            })

            await newPlane.save()

            res.status(201).json({
                message: "El plano creado exitosamente",
                status: true,
            })
        }catch (e: any) {
            res.status(500).json({
                message: "Error al crear el plano",
                status: false,
            })
        }
}

const getPlanes = async (req: Request, res: Response) => {

    const response = await PlaneSchema.find()

    return res.status(200).json({
        message: "Planes obtenidos exitosamente",
        status: true,
        data: response,
    })
}

export {createPlane , getPlanes}