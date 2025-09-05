import {defineStore} from "pinia";
import {ref} from "vue";


export const useUsuariosStore = defineStore('usuariosStore', () => {
    const dataSource = ref([])
    const columns = ref(
        [
            {
                title: "Nombre",
                dataIndex: "name",
                key: "name"
            },
            {
                title: "Correo",
                dataIndex: "email",
                key: "email"
            }
        ]
    )

    return {dataSource, columns}
})