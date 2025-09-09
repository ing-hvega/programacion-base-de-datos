import { requestService } from "@/utils/request.utils.js";

export const useLoginService = {
    authLogin,
};

function authLogin(attributes) {
    return requestService.post("/api/login", { ...attributes });
}
