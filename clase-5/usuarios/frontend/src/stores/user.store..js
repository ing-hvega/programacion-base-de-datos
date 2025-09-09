import {ref} from "vue";
import {defineStore} from "pinia";

const initialFormState = {
    name: '',
    email: '',
    password: '',
    type: undefined,
    description: '',
};

export const useUsersStore = defineStore('userStore', () => {
    const form = ref({...initialFormState})
    const openForm = ref(false)
    const loading = ref(false)
    const dataSource = ref([])
    const pagination = ref({})

    const resetForm = () => {
        form.value = {...initialFormState};
    }

    return {form, pagination, openForm, loading, dataSource, resetForm}
})