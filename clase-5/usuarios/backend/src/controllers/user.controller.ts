import {Request, Response} from "express";
import UserSchema from "../models/user.schema";
import bcrypt from "bcrypt";

const createUser = async (req: Request, res: Response) => {
    try {
        const {name, email, password, type, description}: any = req.body;

        const salt = await bcrypt.genSalt(12);
        const hashedPassword = await bcrypt.hash(password, salt);

        const newUser = new UserSchema({
            name,
            email,
            type,
            description,
            password: hashedPassword
        })

        await newUser.save();

        res.status(201).json({
            message: "Usuario creado exitosamente",
            status: true
        })
    } catch (e: any) {
        console.error("Error al crear usuario:", e.message);
        res.status(500).json(
            {
                message: "Error al crear usuario",
                error: e.message,
                status: false
            }
        )
    }
}

const updateUser = async (req: Request, res: Response) => {
}

const deleteUser = async (req: Request, res: Response) => {
}

const getUsers = async (req: Request, res: Response) => {
    try {

        const response = await UserSchema.find().select({name: 1, email: 1, type: 1, description: 1});

        return res.status(200).json({
            message: "Usuarios obtenidos exitosamente",
            status: true,
            data: response,
        })

    } catch (e: any) {
        console.error("Error al obtener usuarios:", e.message);
    }
}

const getUserById = async (req: Request, res: Response) => {
}

export {createUser, updateUser, deleteUser, getUsers, getUserById}