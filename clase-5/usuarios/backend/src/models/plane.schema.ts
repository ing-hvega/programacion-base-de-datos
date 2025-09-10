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
    state: Boolean,
    created_at: {
        type: Date,
        default: Date.now,
    },
    updated_at: {
        type: Date,
    },
    delete_at: {
        type: Date,
    },
    created_by: {
        type: Schema.Types.ObjectId,
        ref: 'UserSchema',
    },
    updated_by: {
        type: Schema.Types.ObjectId,
        ref: 'UserSchema',
    },
    deleted_by: {
        type: Schema.Types.ObjectId,
    }
})

export default mongoose.model('PlaneSchema', PlaneSchema, 'plane')