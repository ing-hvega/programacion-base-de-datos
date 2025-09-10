import {ref} from "vue"
import {defineStore} from "pinia";

const initialFormState = {
    name: '',
    version: '',
    router_file: '',
    state: false
}

const usePlaneStore = defineStore('planeStore', () => {
    const form = ref(initialFormState)
    const dataSource = ref([])
    const openForm = ref(false)


    return {form, dataSource, openForm}
})

export default usePlaneStore
