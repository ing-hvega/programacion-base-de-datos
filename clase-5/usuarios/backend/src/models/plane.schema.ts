import mongoose, {Schema} from "mongoose";

const PlaneSchema = new Schema({
    name: {
        type: String,
        required: true,
    },
    version: {
        type: String,
        required: true,
    },
    router_file: String,
    state: Boolean
})

export default mongoose.model('PlaneSchema', PlaneSchema, 'plane')