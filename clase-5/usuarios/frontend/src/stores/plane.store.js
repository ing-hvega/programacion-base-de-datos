import {ref} from "vue"
import {defineStore} from "pinia";

const initialFormState = {
    id: undefined,
    name: '',
    version: '',
    router_file: '',
    state: false,
    created_at: undefined,
    updated_at: undefined,
    deleted_at: undefined,
    created_by: undefined,
    updated_by: undefined,
    deleted_by: undefined,
}

const usePlaneStore = defineStore('planeStore', () => {
    const form = ref(initialFormState)
    const dataSource = ref([])
    const openForm = ref(false)
    const isEdit = ref(false)


    return {form, dataSource, openForm, isEdit}
})

export default usePlaneStore
