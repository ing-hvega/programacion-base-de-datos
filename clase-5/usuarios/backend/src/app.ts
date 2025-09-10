import {connectDB} from "./config/database-mongo.config";
import {configDotenv} from "dotenv";
import cors from 'cors';
import express from "express";
import userRouter from "./routes/user.router";
import loginRouter from "./routes/login.router";
import planeRouter from "./routes/plane.router";

configDotenv()

const PORT = process.env.PORT || 3000;

const app = express()

app.use(cors());
app.use(express.json())

connectDB()

app.get('/', (req, res) => res.send('ok!'))
app.use('/api', userRouter)
app.use('/api', loginRouter)
app.use('/api', planeRouter)

app.listen(PORT, () => console.log('Server running on port 3000'))