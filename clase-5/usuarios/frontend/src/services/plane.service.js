import { requestService } from '@/utils/request.utils.js';

export const usePlaneService = {
    createPlane,
    getAllPlane
}

function getPlanes() {}

function createPlane(attributes) {
    return requestService.post('/api/plane', {...attributes});
}

function getAllPlane() {
    return requestService.get('/api/planes');
}