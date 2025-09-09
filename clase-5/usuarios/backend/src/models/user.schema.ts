import mongoose, {Schema} from "mongoose";

const UserSchema = new Schema({
    name: {
        type: String,
        required: true,
    },
    email: {
        type: String,
        required: true,
        unique: true,
    },
    password: String,
    type: Number,
    description: String,
})

export default mongoose.model('UserSchema', UserSchema, 'users')
