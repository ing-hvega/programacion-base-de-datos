import {Request, Response} from "express";
import UserSchema from "../../models/mongodb/user.schema";
import bcrypt from "bcrypt";
import jwt from "jsonwebtoken";

const authLogin = async (req: Request, res: Response) => {

    const {email, password} = req.body;

    const user: any = await UserSchema.findOne({email: email}, {password: 1, email: 1, type: 1});

    if (!user) {
        return res.status(401).json({
            message: "Credenciales incorrectas",
            status: false
        })
    }

    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) {
        return res.status(401).json({
            message: "Credenciales incorrectas",
            status: false
        })
    }

    const token = jwt.sign(
        { id: user._id, email: user.email, type: user.type },
        process.env.JWT_SECRET || '',
        { expiresIn: '1d' }
    );

    return res.status(200).json({
        message: "Login exitoso",
        status: true,
        token: token
    })
}

export {authLogin}