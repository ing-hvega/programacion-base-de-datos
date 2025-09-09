import mongoose from "mongoose";

export const connectDB = async () => {

    try {
        const mongoURI: string = process.env.MONGODB_URI || '';

        console.info('Intentando conectar a MongoDB...');

        await mongoose.connect(mongoURI);

        console.info("Conectado a MongoDB exitosamente")
    } catch (e: any) {
        console.error("Error al conectar a MongoDB:", e.message);
    }
}

mongoose.connection.on('error', (error) => {
    console.error(`Error de conexión a MongoDB: ${error}`);
});
