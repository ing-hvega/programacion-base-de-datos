import { requestService } from "@/utils/request.utils.js";

export const useUserService = {
    createUser,
    updateUser,
    deleteUser,
    showUser,
    listUsers,
};

function createUser(attributes) {
    return requestService.post("/api/user", { ...attributes });
}

function updateUser(id, attributes) {
    return requestService.put(`/api/user/${id}`, { ...attributes });
}

function deleteUser(id) {
    return requestService.delete(`/api/user/${id}`);
}

function showUser(id) {
    return requestService.get(`/api/user/${id}`);
}

function listUsers() {
    return requestService.get(`/api/users`);
}
