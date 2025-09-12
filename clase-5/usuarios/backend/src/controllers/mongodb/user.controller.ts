import {Request, Response} from "express";
import UserSchema from "../../models/mongodb/user.schema";
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
        const { page = '1', pageSize = '10', search } = req.query;
        const pageNum = parseInt(page as string);
        const pageSizeNum = parseInt(pageSize as string);

        const skipIndex = (pageNum - 1) * pageSizeNum;

        const filter: any = {};
        if (search) {
            const searchRegex = new RegExp(search as string, 'i');

            filter.$or = [
                { name: { $regex: searchRegex } },
                { email: { $regex: searchRegex } }
            ];
        }

        const response = await UserSchema
            .find(filter)
            .select({name: 1, email: 1, type: 1, description: 1})
            .skip(skipIndex)
            .limit(pageSizeNum)
            .lean();

        const total = await UserSchema.countDocuments(filter);

        return res.status(200).json({
            message: "Usuarios obtenidos exitosamente",
            status: true,
            data: response,
            pagination: {
                page: pageNum,
                pageSize: pageSizeNum,
                total,
                totalPages: Math.ceil(total / pageSizeNum)
            }
        });

    } catch (e: any) {
        console.error("Error al obtener usuarios:", e.message);
        return res.status(500).json({
            message: "Error al obtener usuarios",
            error: e.message,
            status: false
        });
    }
}

const getUserById = async (req: Request, res: Response) => {
}

export {createUser, updateUser, deleteUser, getUsers, getUserById}