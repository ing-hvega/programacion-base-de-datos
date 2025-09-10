import { requestService } from '@/utils/request.utils.js';

export const usePlaneService = {
    createPlane,
    getAllPlane,
    updatePlane,
    getPlane,
    deletePlane,
}

function getPlane(id) {
    return requestService.get(`/api/plane/${id}`);
}

function createPlane(attributes) {
    return requestService.post('/api/plane', {...attributes});
}

function updatePlane(id, attributes) {
    return requestService.put(`/api/plane/${id}`, {...attributes});
}

function deletePlane(id) {
    return requestService.delete(`/api/plane/${id}`);
}

function getAllPlane() {
    return requestService.get('/api/planes');
}