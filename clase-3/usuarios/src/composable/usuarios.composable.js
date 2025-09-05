import {useUsuariosStore} from "@/stores/usuarios.store.js";
import {storeToRefs} from "pinia";
import {useUsuariosServices} from "@/services/usuarios.services.js";
import {onMounted} from "vue";


export function useUsuariosComposable() {

    const usuariosStore = useUsuariosStore()

    const {getUsuarios} = useUsuariosServices

    const { dataSource, columns } = storeToRefs(usuariosStore)

    onMounted(async () => {
        const response = await getUsuarios()

        console.log(response)

        dataSource.value = response
    })


    return {
        dataSource,
        columns
    }

}