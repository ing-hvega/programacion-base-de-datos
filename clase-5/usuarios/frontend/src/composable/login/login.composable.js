import {storeToRefs} from "pinia";
import {useLoginStore} from "@/stores/login.store..js";
import {useLoginService} from "@/services/login.service..js";
import {message} from "ant-design-vue";
import {useRouter} from 'vue-router';

export function useLoginComposable() {
    const loginStore = useLoginStore()
    const router = useRouter();

    const {form, loading} = storeToRefs(loginStore)

    const handleAuthSession = async () => {
        const keyMessage = 'key_auth'
        loading.value = true

        try {
            const {status, token} = await useLoginService.authLogin({...form.value})

            if (!status) {
                throw new Error("Autenticación fallida")
            }

            localStorage.setItem("token", token);
            message.success({
                content: "Inicio de sesión exitoso. Redirigiendo...",
                key: keyMessage
            }, 5)

            await new Promise(resolve => setTimeout(resolve, 1000))
            await router.push({name: 'home'})
        } catch (e) {
            message.error({
                content: "No puede iniciar sesión, contáctese con un administrador",
                key: keyMessage
            }, 5)
        } finally {
            loading.value = false
        }
    }

    return {
        form,
        loading,
        handleAuthSession,
    }
}