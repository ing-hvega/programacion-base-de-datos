import {requestService} from "@/utils/request.utils.js";


export const useUsuariosServices = {
 getUsuarios
}

function getUsuarios() {
    return requestService.get("/users")
}