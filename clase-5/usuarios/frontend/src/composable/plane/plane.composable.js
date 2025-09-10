import {storeToRefs} from 'pinia'
import usePlaneStore from '@/stores/plane.store.js'
import {usePlaneService} from "@/services/plane.service.js"
import {onMounted} from "vue";

export function usePlaneComposable() {

    const planeStore = usePlaneStore()

    const {form, dataSource, openForm, isEdit} = storeToRefs(planeStore)

    const {createPlane, getAllPlane, updatePlane, deletePlane, getPlane} = usePlaneService

    const handleCreateOrUpdatePlane = async () => {
        if (isEdit.value) {
            form.value.created_at = Date.now()
            form.value.created_by = Date.now()
            await updatePlane(form.value.id, form.value)
        } else {
            await createPlane(form.value)
        }

        handleCloseForm()
        await setPlanes()
    }

    const handleOpenForm = () => {
        openForm.value = true
    }

    const handleCloseForm = () => {
        openForm.value = false
        isEdit.value = false
    }

    const handleEdit = async (id) => {
        isEdit.value = true
        form.value.id = id

        const response = await getPlane(id)
        form.value.name = response.data.name
        form.value.state = Number(response.data.state)
        form.value.version = response.data.version
        form.value.router_file = response.data.router_file
        handleOpenForm()
    }

    const handleDelete = async (id) => {
        await deletePlane(id)
        await setPlanes()
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
        },
        {
            title: 'Opciones',
            dataIndex: 'options',
            key: 'options',
            width: '8%',
            align: 'center'
        }
    ]

    return {
        form,
        dataSource,
        handleCreateOrUpdatePlane,
        columns,
        openForm,
        handleOpenForm,
        handleCloseForm,
        handleEdit,
        handleDelete,
        isEdit
    }

}