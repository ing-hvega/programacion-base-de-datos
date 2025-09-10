import { storeToRefs } from 'pinia'
import usePlaneStore from '@/stores/plane.store.js'
import {usePlaneService} from "@/services/plane.service.js"
import { onMounted } from "vue";

export function usePlaneComposable() {

    const planeStore = usePlaneStore()

    const {form, dataSource, openForm} = storeToRefs(planeStore)

    const { createPlane, getAllPlane } = usePlaneService

    const handleCreatePlane = async () => {
       const response = await createPlane(form.value)
        handleCloseForm()
        setPlanes()
    }

    const handleOpenForm = () => {
        openForm.value = true
    }

    const handleCloseForm = () => {
        openForm.value = false
    }

    const setPlanes = async () => {
        const response = await getAllPlane()
        dataSource.value = response.data
    }

    onMounted(async () => {
        setPlanes()
    })

    const columns = [
        {
            title: 'Nombre',
            dataIndex: 'name',
            key: 'name'
        },
        {
            title: 'Nueva version',
            dataIndex: 'version',
            key: 'version'
        }
    ]


    return { form, dataSource, handleCreatePlane, columns, openForm, handleOpenForm, handleCloseForm }

}