import {ref} from "vue";
import {defineStore} from "pinia";

export const useLoginStore = defineStore('loginStore', () => {
    const form = ref({
        email: '',
        password: '',
    })
    const loading = ref(false)

    return {form, loading}
})