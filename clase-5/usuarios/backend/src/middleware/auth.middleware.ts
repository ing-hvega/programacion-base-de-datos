import {NextFunction, Request, Response} from "express";
import jwt from "jsonwebtoken";

interface AuthRequest extends Request {
    user?: any;
}

const authMiddleware = (req: AuthRequest, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;

    if (!authHeader) {
        return res.status(401).json({
            message: "No se proporcionó token de autenticación"
        });
    }

    const token = authHeader.split(" ")[1];

    if (!token) {
        return res.status(401).json({
            message: "Formato de token inválido"
        });
    }

    try {
        req.user = jwt.verify(token, process.env.JWT_SECRET || '');

        next();
    } catch (error) {
        return res.status(401).json({
            message: "Token inválido o expirado"
        });
    }
};

export default authMiddleware;
